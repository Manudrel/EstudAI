from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage
from langchain_core.messages import HumanMessage

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
            model="openai/gpt-oss-120b",
            temperature=0.3,
            max_tokens=2000
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

            # Caso não haja chamadas de ferramentas, finaliza o loop e retorna o relatório
            if not response.tool_calls:
                print("\n=== FINAL REPORT ===")
                print(response.content[:1000])

                if len(research_memory) == 0:
                    messages.append(
                        (
                            "human",
                            """
                            Você ainda não realizou nenhuma pesquisa.

                            Utilize pelo menos uma ferramenta antes de gerar
                            o relatório final.
                            """
                        )
                    )                 
                    continue

                return ResearchReport(
                    report=response.content
                    if response.content
                    else "Nenhum relatório foi gerado.",
                    research_steps=[
                        ResearchStep(**step)
                        for step in research_memory
                    ]
                )
            

            messages.append(response)

            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                if tool_name == "web_search":    
                    if "query" not in tool_args:

                            messages.append(
                                ToolMessage(
                                    content=(
                                        "Erro: a ferramenta web_search "
                                        "exige o parâmetro 'query'. "
                                        "Tente novamente."
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
                        f"Tool já executada: {tool_name}"
                    )

                    messages.append(
                        ToolMessage(
                            content=(
                                "Esta busca já foi executada anteriormente. "
                                "Utilize as informações já obtidas e gere "
                                "o relatório final."
                            ),
                            tool_call_id=tool_call["id"]
                        )
                    )

                    continue

                executed_calls.add(
                    call_signature
                )

                print(
                    f"\nExecutando Tool: {tool_name}"
                )
                print(
                    f"Args: {tool_args}"
                )

                tool = TOOLS.get(
                    tool_name
                )

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
                            f"Erro ao executar "
                            f"{tool_name}: {str(e)}"
                        )

                tool_result_str = str(
                    tool_result
                )

                if len(tool_result_str) > MAX_TOOL_RESULT:

                    tool_result_str = (
                        tool_result_str[
                            :MAX_TOOL_RESULT
                        ]
                        + "\n\n[RESULTADO TRUNCADO]"
                    )

                messages.append(
                    ToolMessage(
                        content=tool_result_str,
                        tool_call_id=tool_call["id"]
                    )
                )
                print("\n===  TOOL RESULT  ===")
                print(tool_result_str[:500])

                research_memory.append(
                    {
                        "tool": tool_name,
                        "args": tool_args,
                        "result": tool_result_str[:1000]
                    }
                )

            if iteration >= 2:
                break

        final_response = self.llm.invoke(
            messages + [
                HumanMessage(
                    content=(
                        "Com base apenas nas informações já coletadas, "
                        "gere o relatório final completo."
                    )
                )
            ]
        )

        return ResearchReport(
            report=final_response.content,
            research_steps=[
                ResearchStep(**step)
                for step in research_memory
            ]
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