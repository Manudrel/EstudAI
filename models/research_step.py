from pydantic import BaseModel

class ResearchStep(BaseModel):
    tool: str
    args: dict
    result: str