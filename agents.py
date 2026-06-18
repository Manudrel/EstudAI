from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

def agent_prompt(agent_name: str) -> str:
    with open(f"prompts/{agent_name}.txt", "r") as f:
        prompt = f.read()

    return prompt

def search_agent(query: str, context_window: list):

    prompt =agent_prompt("search_agent") + f"\n\nQuery: {query}"

    response = llm.invoke(prompt)

    return response.content



def summarize_agent(query: str, context_window: list):

    prompt =agent_prompt("summarize_agent") + f"\n\nQuery: {query}"

    response = llm.invoke(prompt)

    return response.content


def quiz_agent(query: str, context_window: list, search_or_summarize: str | None):

    prompt =agent_prompt("quiz_agent") + f"\n\nQuery: {query}"

    response = llm.invoke(prompt)

    return response.content