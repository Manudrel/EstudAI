from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from models.study_material import StudyMaterial

load_dotenv()


with open(
    "prompts/professor_planning.txt",
    encoding="utf-8"
) as f:
    planning_system = f.read()

with open(
    "prompts/professor_material.txt",
    encoding="utf-8"
) as f:
    material_system = f.read()


planning_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", planning_system),
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
        ("system", material_system),
        (
            "human",
            """
Tema:

{query}

=============================

Plano Pedagógico:

{plan}

=============================

Contexto Científico:

{context}
"""
        )
    ]
)


class ProfessorAgent:

    def __init__(self):

        llm = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0.3,
            max_tokens=4000
        )

        self.planning_chain = planning_prompt | llm

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

        context = "\n\n".join(context_window)

        print(
            "\n=== PROFESSOR :: PEDAGOGICAL PLANNING ==="
        )

        plan = self.planning_chain.invoke(
            {
                "query": query,
                "context": context
            }
        )

        print(plan.content[:800])

        print(
            "\n=== PROFESSOR :: MATERIAL GENERATION ==="
        )

        material = self.material_chain.invoke(
            {
                "query": query,
                "plan": plan.content,
                "context": context
            }
        )

        return material


