import json

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from models.study_material import StudyMaterial

load_dotenv()

with open(
    "prompts/professor_planning.txt",
    "r",
    encoding="utf-8"
) as f:
    planning_system = f.read()

with open(
    "prompts/professor_material.txt",
    "r",
    encoding="utf-8"
) as f:
    material_system = f.read()

with open(
    "prompts/professor_exercise.txt",
    "r",
    encoding="utf-8"
) as f:
    exercise_system = f.read()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3,
    max_tokens=4000
)

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

planning_chain = planning_prompt | llm

material_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", material_system),
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

material_chain = material_prompt | llm

exercise_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", exercise_system),
        (
            "human",
            """
            Tema:
            {query}

            Material:
            {material}

            Contexto:
            {context}
            """
        )
    ]
)

exercise_chain = exercise_prompt | llm


class ProfessorAgent:

    def __init__(self):
        self.planning_chain = planning_chain
        self.material_chain = material_chain
        self.exercise_chain = exercise_chain

    def get_response(
        self,
        query: str,
        context_window: list[str]
    ) -> StudyMaterial:

        context_text = "\n".join(
            context_window
        )

        # STEP 1: PLANNING
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

        # STEP 2: MATERIAL GENERATION
        print(
            "\n=== PROFESSOR STEP 2: MATERIAL GENERATION ==="
        )

        material_response = self.material_chain.invoke(
            {
                "query": query,
                "plan": plan.content,
                "context": context_text
            }
        )

        material_data = json.loads(
            material_response.content
        )

        print(json.dumps(material_data, indent=2)[:1000])

        # STEP 3: EXERCISE GENERATION
        print(
            "\n=== PROFESSOR STEP 3: EXERCISE GENERATION ==="
        )

        exercises_response = self.exercise_chain.invoke(
            {
                "query": query,
                "material": json.dumps(
                    material_data,
                    indent=2
                ),
                "context": context_text
            }
        )

        exercises_data = json.loads(
            exercises_response.content
        )

        print(
            json.dumps(exercises_data, indent=2)[:1000]
        )

        # MERGE AND BUILD StudyMaterial
        material_data["exercises"] = exercises_data[
            "exercises"
        ]

        material = StudyMaterial(**material_data)

        return material



if __name__ == "__main__":

    professor = ProfessorAgent()

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

    response = professor.get_response(
        query="Explique Clean Architecture",
        context_window=[
            report
        ]
    )

    print("\n=== FINAL REVIEWED REPORT ===\n")
    print(response)