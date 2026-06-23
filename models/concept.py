from pydantic import BaseModel, Field


class Concept(BaseModel):

    name: str = Field(
        description="Nome do conceito"
    )

    definition: str = Field(
        description="Definição simples"
    )

    explanation: str = Field(
        description="Explicação detalhada"
    )

    example: str = Field(
        description="Exemplo prático"
    )