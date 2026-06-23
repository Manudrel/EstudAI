from pydantic import BaseModel, Field
from models.question import Question
from models.concept import Concept


class StudyMaterial(BaseModel):

    title: str = Field(
        description="Título atrativo da aula"
    )

    introduction: str = Field(
        description=(
            "Introdução explicando o que é o tema, "
            "por que é importante e onde é utilizado."
        ),
        min_length=300,
    )

    concepts: list[Concept] = Field(
        min_length=3,
        max_length=10,
        description=(
            "Lista dos conceitos fundamentais do tema."
        )
    )

    analogy: str = Field(
        description=(
            "Analogia simples e memorável "
            "para facilitar o entendimento."
        ),
        min_length=100
    )

    applications: str = Field(
        description=(
            "Aplicações práticas e exemplos reais "
            "de uso do conceito."
        ),
        min_length=200
    )

    tip: str = Field(
        description="Dica prática do professor.",
        min_length=50
    )

    summary_points: list[str] = Field(
        min_length=5,
        max_length=10,
        description="Resumo dos principais aprendizados."
    )

    exercises: list[Question] = Field(
        min_length=5,
        max_length=5,
        description=(
            "Exatamente 5 exercícios: "
            "2 easy, 2 medium e 1 hard."
        )
    )