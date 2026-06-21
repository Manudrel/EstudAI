from pydantic import BaseModel
from models.research_step import ResearchStep

class ResearchReport(BaseModel):
    report: str
    research_steps: list[ResearchStep]