from pydantic import BaseModel, Field
from models.question import Question
from models.concept import Concept


class StudyMaterial(BaseModel):

    title: str = Field(
        description="Título atrativo da aula"
    )

    introduction: str = Field(
        description=(
            "Introdução"
            "por que é importante e onde é utilizado."
        ),
    )

    concepts: list[Concept] = Field(
        max_length=10,
        description=(
            "Lista dos conceitos fundamentais do tema."
        )
    )

    analogy: str = Field(
        description=(
            "Analogia simples e memorável "
            "para facilitar o entendimento."
        )    
    )

    applications: str = Field(
        description=(
            "Aplicações práticas e exemplos reais "
            "de uso do conceito."
        )
    )

    tip: str = Field(
        description="Dica prática do professor.",
    )

    summary_points: list[str] = Field(
        max_length=10,
        description="Resumo dos principais aprendizados."
    )

    exercises: list[Question] = Field(
        max_length=5,
        description=(
            "Exatamente 5 exercícios: "
            "2 easy, 2 medium e 1 hard."
        )
    )