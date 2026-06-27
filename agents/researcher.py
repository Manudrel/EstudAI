from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import (
    ToolMessage,
)

from tools.arxiv_tool import search_arxiv
from tools.web_search_tool import web_search
from tools.pdf_tool import read_pdf

from models.research_report import ResearchReport
from models.research_step import ResearchStep

load_dotenv()

MAX_TOOL_RESULT = 4000


with open(
    "prompts/researcher_system.txt",
    "r",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()

with open(
    "prompts/researcher_planning.txt",
    "r",
    encoding="utf-8"
) as f:
    PLANNING_PROMPT = f.read()

with open(
    "prompts/researcher_synthesis.txt",
    "r",
    encoding="utf-8"
) as f:
    SYNTHESIS_PROMPT = f.read()


planning_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", PLANNING_PROMPT),
        ("human", "{query}")
    ]
)

research_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "system",
            """
Plano de Pesquisa

{plan}
            """
        ),
        ("human", "{query}")
    ]
)

synthesis_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYNTHESIS_PROMPT),
        (
            "human",
            """
Tema:

{query}

================================

Evidências Coletadas:

{memory}
"""
        )
    ]
)


TOOLS = {
    "search_arxiv": search_arxiv,
    "web_search": web_search,
    "read_pdf": read_pdf,
}


class ResearcherAgent:

    def __init__(self):

        self.llm = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0.3,
            max_tokens=2000
        )

        self.llm_with_tools = self.llm.bind_tools(
            list(TOOLS.values())
        )

        self.planning_chain = (
            planning_prompt
            | self.llm
        )

        self.synthesis_chain = (
            synthesis_prompt
            | self.llm
        )

    def _execute_tool(
        self,
        tool_name,
        tool_args
    ):

        tool = TOOLS.get(tool_name)

        if tool is None:

            return (
                f"Tool '{tool_name}' não encontrada."
            )

        try:

            result = tool.invoke(
                tool_args
            )

        except Exception as e:

            result = (
                f"Erro ao executar "
                f"{tool_name}: {str(e)}"
            )

        result = str(result)

        if len(result) > MAX_TOOL_RESULT:

            result = (
                result[:MAX_TOOL_RESULT]
                + "\n\n[RESULTADO TRUNCADO]"
            )

        return result

    def get_response(
        self,
        query: str
    ) -> ResearchReport:


        print("\n=== RESEARCH PLANNING ===")

        plan = self.planning_chain.invoke(
            {
                "query": query
            }
        )

        print(plan.content[:1000])


        messages = research_prompt.format_messages(
            query=query,
            plan=plan.content
        )

        research_memory = []
        executed_calls = set()

        max_iterations = 4

        for iteration in range(max_iterations):

            print(f"\n=== ITERATION {iteration + 1} ===")

            response = self.llm_with_tools.invoke(
                messages
            )

            print("\n=== RESPONSE CONTENT ===")
            print(response.content)

            print(
                "Tool calls:",
                response.tool_calls
            )

        
            if not response.tool_calls:

                if len(research_memory) == 0:

                    messages.append(
                        (
                            "human",
                            """
                            Você ainda não utilizou nenhuma ferramenta.

                            Utilize pelo menos uma ferramenta antes
                            de finalizar a pesquisa.
                            """
                        )
                    )

                    continue

                break

            messages.append(response)

         

            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                if (
                    tool_name == "web_search"
                    and "query" not in tool_args
                ):

                    messages.append(

                        ToolMessage(

                            content=(
                                "Erro: web_search "
                                "necessita do parâmetro "
                                "'query'."
                            ),

                            tool_call_id=tool_call["id"]

                        )

                    )

                    continue

                call_signature = (
                    tool_name,
                    str(tool_args)
                )

                if call_signature in executed_calls:

                    print(
                        f"Pesquisa repetida: {tool_name}"
                    )

                    messages.append(

                        ToolMessage(

                            content=(
                                "Esta pesquisa já foi "
                                "realizada anteriormente."
                            ),

                            tool_call_id=tool_call["id"]

                        )

                    )

                    continue

                executed_calls.add(
                    call_signature
                )

                print(
                    f"\nExecutando {tool_name}"
                )

                print(tool_args)

                tool_result = self._execute_tool(
                    tool_name,
                    tool_args
                )

                print(
                    "\n=== TOOL RESULT ==="
                )

                print(tool_result[:500])

                messages.append(

                    ToolMessage(

                        content=tool_result,

                        tool_call_id=tool_call["id"]

                    )

                )

                research_memory.append(

                    {

                        "tool": tool_name,

                        "args": tool_args,

                        "result": tool_result[:1000]

                    }

                )


        print("\n=== SYNTHESIS ===")

        memory = "\n\n".join(

            [

                f"""
                Ferramenta:
                {step['tool']}

                Parâmetros:
                {step['args']}

                Resultado:

                {step['result']}
                """

                for step in research_memory

            ]

        )

        final_report = self.synthesis_chain.invoke(

            {

                "query": query,

                "memory": memory

            }

        )

        print(
            "\n=== FINAL REPORT ==="
        )

        print(
            final_report.content[:1000]
        )

        return ResearchReport(

            report=final_report.content,

            research_steps=[

                ResearchStep(**step)

                for step in research_memory

            ]

        )


if __name__ == "__main__":

    researcher = ResearcherAgent()

    report = researcher.get_response(
        """
        Search for scientific papers about
        Attention Is All You Need.

        Explain:

        - Main contributions
        - Architecture
        - Impact on modern LLMs
        """
    )

    print("\n=== REPORT ===\n")

    print(report)