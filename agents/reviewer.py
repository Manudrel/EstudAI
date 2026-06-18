from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

template = ChatPromptTemplate(
    [
        ("system", ...),
        ("query", "Researcher Output: {query}"),
        ("context_window", "Context window: {context_window}")
    ]
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)


class ReviewerAgent:

    def __init__(self, name: str):
        self.name = name


    def get_response(self, query: str, context_window: list):

        prompt = template.format_messages(query=query, context_window=context_window)

        response = llm.invoke(prompt)

        return response.content