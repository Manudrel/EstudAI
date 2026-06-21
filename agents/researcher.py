from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage

from tools.arxiv_tool import search_arxiv
from tools.web_search_tool import web_search
from tools.pdf_tool import read_pdf

from models.research_report import ResearchReport
from models.research_step import ResearchStep

load_dotenv()

MAX_TOOL_RESULT = 2000

with open(
    "prompts/researcher_system.txt",
    "r",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()


PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{query}")
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
            model="llama-3.1-8b-instant",
            temperature=0.3
        )

        self.llm_with_tools = self.llm.bind_tools(
            list(TOOLS.values())
        )


    def get_response(self, query: str) -> ResearchReport:

        research_memory = []
        
        executed_calls = set()

        messages = PROMPT.format_messages(
            query=query
        )

        max_iterations = 5

        for iteration in range(max_iterations):

            response = self.llm_with_tools.invoke(
                messages
            )

            print(f"\n=== ITERATION {iteration + 1} ===")
            print("Tool calls:", response.tool_calls)

            # Caso não haja chamadas de ferramentas, retorna a resposta final
            if not response.tool_calls:

                if response.content:
                    return ResearchReport(
                        report=response.content,
                        research_steps=[ResearchStep(**step) for step in research_memory]
                    )

                return ResearchReport(
                    report="Nenhuma resposta foi gerada.",
                    research_steps=[
                        ResearchStep(**step)
                        for step in research_memory
                    ]
                )

            messages.append(response)

            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                call_signature = (
                    tool_name,
                    str(tool_args)
                )

                if call_signature in executed_calls:

                    print(
                        f"Tool já executada: {tool_name}"
                    )

                    continue

                executed_calls.add(call_signature)

                print(f"\nExecutando Tool: {tool_name}")
                print(f"Args: {tool_args}")

                tool = TOOLS.get(tool_name)

                if not tool:

                    tool_result = (
                        f"Tool '{tool_name}' não encontrada."
                    )

                else:

                    try:
                        tool_result = tool.invoke(
                            tool_args
                        )


                    except Exception as e:

                        tool_result = (
                            f"Erro ao executar tool "
                            f"{tool_name}: {str(e)}"
                        )



                        tool_result_str = str(tool_result)

                        if len(tool_result_str) > MAX_TOOL_RESULT:
                            tool_result_str = (
                                tool_result_str[:MAX_TOOL_RESULT]
                                + "\n\n[RESULTADO TRUNCADO]"
                            )

                        messages.append(
                            ToolMessage(
                                content=tool_result_str,
                                tool_call_id=tool_call["id"]
                            )
                        )

                research_memory.append(
                    {
                        "tool": tool_name,
                        "args": tool_args,
                        "result": str(tool_result)[:1000]
                    }
                )

        return ResearchReport(
            report="Limite máximo de interações com ferramentas atingido.",
            research_steps=[ResearchStep(**step) for step in research_memory]
        )


if __name__ == "__main__":

    researcher = ResearcherAgent()

    response = researcher.get_response(
        """
        Search for scientific papers about
        Attention Is All You Need.

        Explain:
        - Main contributions
        - Architecture
        - Impact on modern LLMs
        """
    )

    print("\n=== RESEARCH REPORT ===\n")
    print(response)