from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

with open("prompts/reviewer_system.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("system", "Context Window:\n{context_window}"),
        ("human", "Input: {query}")
    ]
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)


class ReviewerAgent:
    def __init__(self, name: str):
        self.name = name

    def get_response(self, query: str, context_window: list[str]) -> str:
        context_text = "\n".join(context_window)

        messages = template.format_messages(
            query=query,
            context_window=context_text
        )

        response = llm.invoke(messages)

        return response.content


if __name__ == "__main__":
    reviewer = ReviewerAgent("Reviewer")

    query = "What are the main contributions of the paper 'Attention is All You Need'?"

    context_window = [
        "The paper introduces the Transformer architecture, which relies entirely on self-attention mechanisms, dispensing with recurrent and convolutional layers.",
        "The Transformer achieves state-of-the-art performance in various natural language processing tasks.",
        "The architecture became the foundation for modern LLMs such as GPT, LLaMA, Claude and Gemini."
    ]

    response = reviewer.get_response(
        query=query,
        context_window=context_window
    )

    print("\n=== REVIEWER RESPONSE ===\n")
    print(response)