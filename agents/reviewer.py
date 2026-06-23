from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

with open("prompts/reviewer_system.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Input: {query}")
    ]
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    max_tokens=1500
)


class ReviewerAgent:

    def get_response(self, research_report: str) -> str:

        messages = template.format_messages(
            query=research_report,
        )

        response = llm.invoke(messages)

        return response.content


if __name__ == "__main__":
    reviewer = ReviewerAgent("Reviewer")

    research_report = "What are the main contributions of the paper 'Attention is All You Need'?"

    response = reviewer.get_response(
        query=research_report,
    )

    print("\n=== REVIEWER RESPONSE ===\n")
    print(response)