# services/orchestrator.py

from agents.researcher import ResearcherAgent
from agents.reviewer import ReviewerAgent
from agents.professor import ProfessorAgent


class StudyOrchestrator:

    def __init__(self):

        self.researcher = ResearcherAgent()
        self.reviewer = ReviewerAgent()
        self.professor = ProfessorAgent()

    def execute(self, topic: str, callback=None) -> dict:

        research_report = (
            self.researcher.get_response(topic)
        )

        reviewed_report = (
            self.reviewer.get_response(
                research_report.report
            )
        )

        study_material = (
            self.professor.get_response(
                query=topic,
                context_window=[reviewed_report]
            )
        )

        return {
            "research": research_report,
            "review": reviewed_report,
            "lesson": study_material
        }
    
if __name__ == "__main__":
    orchestrator = StudyOrchestrator()

    topic = "Explique o teorema de Pitágoras."

    result = orchestrator.execute(topic)

    print(result)