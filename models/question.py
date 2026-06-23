from typing import Literal
from pydantic import BaseModel, Field


class Question(BaseModel):

    question: str

    difficulty: Literal[
        "easy",
        "medium",
        "hard"
    ]

    answer: str = Field(
        description="Resposta correta e explicada"
    )