from pydantic import BaseModel, Field

class Question(BaseModel):

    question: str = Field(
        description="Pergunta para o aluno"
    )

    difficulty: str = Field(
        description="easy, medium ou hard"
    )

    answer: str = Field(
        description="Resposta correta"
    )