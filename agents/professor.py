from dotenv import load_dotenv
import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from models.study_material import StudyMaterial

load_dotenv()

with open(
    "prompts/professor_system.txt",
    "r",
    encoding="utf-8"
) as f:
    system_prompt = f.read()


template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("system", "Context Window:\n{context_window}"),
        ("human", "Input: {query}")
    ]
)


class ProfessorAgent:

    def __init__(self):

        self.llm = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0.3
        )

    def get_response(
        self,
        query: str,
        context_window: list[str]
    ) -> StudyMaterial:

        context_text = "\n".join(
            context_window
        )

        messages = template.format_messages(
            query=query,
            context_window=context_text
        )

        response = self.llm.invoke(
            messages
        )

        try:

            return StudyMaterial.model_validate_json(
                response.content
            )

        except Exception:

            try:

                return StudyMaterial.model_validate(
                    json.loads(response.content)
                )

            except Exception as e:

                print("\n========== RAW RESPONSE ==========\n")
                print(response.content)
                print("\n==================================\n")

                raise RuntimeError(
                    f"Erro ao converter JSON para StudyMaterial:\n{e}"
                )
if __name__ == "__main__":
    professor = ProfessorAgent()
    
    context = [
        "The Pythagorean theorem states that in a right triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides."
    ]

    response = professor.get_response(
        query="Explain the Pythagorean theorem.",
        context_window=context
    )

    print(response)