from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from models.study_material import StudyMaterial

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3
)


planning_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Você é um professor especialista.

            Analise o conteúdo recebido
            e monte um plano de ensino.
            """
        ),
        (
            "human",
            """
            Tema:
            {query}

            Contexto:
            {context}
            """
        )
    ]
)

material_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Você é um professor.

            Gere material de estudo completo
            seguindo exatamente o schema solicitado.
            """
        ),
        (
            "human",
            """
            Tema:
            {query}

            Plano:
            {plan}

            Contexto:
            {context}
            """
        )
    ]
)


class ProfessorAgent:

    def __init__(self):

        self.planning_chain = (
            planning_prompt
            | llm
        )

        self.material_chain = (
            material_prompt
            | llm.with_structured_output(
                StudyMaterial
            )
        )

    def get_response(
        self,
        query: str,
        context_window: list[str]
    ) -> StudyMaterial:

        context_text = "\n".join(
            context_window
        )

        print(
            "\n=== PROFESSOR STEP 1: PLANNING ==="
        )

        plan = self.planning_chain.invoke(
            {
                "query": query,
                "context": context_text
            }
        )

        print(plan.content[:1000])

        print(
            "\n=== PROFESSOR STEP 2: MATERIAL GENERATION ==="
        )

        material = self.material_chain.invoke(
            {
                "query": query,
                "plan": plan.content,
                "context": context_text
            }
        )

        return material