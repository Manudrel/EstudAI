from pydantic import BaseModel
from models.question import Question

class StudyMaterial(BaseModel):
    title: str
    introduction: str
    explanation: str
    analogy: str
    applications: str
    tip: str
    summary_points: list[str]
    exercises: list[Question]