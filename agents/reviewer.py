from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


with open(
    "prompts/reviewer_critique.txt",
    "r",
    encoding="utf-8"
) as f:
    critique_system = f.read()

with open(
    "prompts/reviewer_validation.txt",
    "r",
    encoding="utf-8"
) as f:
    validation_system = f.read()

with open(
    "prompts/reviewer_rewrite.txt",
    "r",
    encoding="utf-8"
) as f:
    rewrite_system = f.read()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    max_tokens=1500
)

critique_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", critique_system),
        ("human", "{report}")
    ]
)

critique_chain = critique_prompt | llm

validation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", validation_system),
        (
            "human",
            """
            RELATÓRIO:

            {report}

            ---------------------

            ANÁLISE CRÍTICA:

            {critique}
            """
        )
    ]
)

validation_chain = validation_prompt | llm

rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rewrite_system),
        (
            "human",
            """
            RELATÓRIO ORIGINAL:

            {report}

            ---------------------

            PLANO DE CORREÇÃO:

            {validation}
            """
        )
    ]
)

rewrite_chain = rewrite_prompt | llm

class ReviewerAgent:

    def __init__(self):

        self.critique_chain = critique_chain
        self.validation_chain = validation_chain
        self.rewrite_chain = rewrite_chain

    def get_response(
        self,
        research_report: str
    ) -> str:

        print("\n=== REVIEW STEP 1: CRITIQUE ===")

        critique = self.critique_chain.invoke(
            {
                "report": research_report
            }
        )

        print(critique.content[:1000])

        print("\n=== REVIEW STEP 2: VALIDATION ===")

        validation = self.validation_chain.invoke(
            {
                "report": research_report,
                "critique": critique.content
            }
        )

        print(validation.content[:1000])

        print("\n=== REVIEW STEP 3: REWRITE ===")

        revised_report = self.rewrite_chain.invoke(
            {
                "report": research_report,
                "validation": validation.content
            }
        )

        return revised_report.content



if __name__ == "__main__":

    reviewer = ReviewerAgent()

    report = """
    Attention Is All You Need foi publicado em 2017.

    O trabalho introduziu a arquitetura Transformer.

    O Transformer substituiu completamente
    as redes neurais existentes.

    O artigo teve grande impacto na área de IA.

    O Transformer utiliza atenção.
    O Transformer utiliza atenção.
    O Transformer utiliza atenção.
    """

    response = reviewer.get_response(
        report
    )

    print("\n=== FINAL REVIEWED REPORT ===\n")
    print(response)