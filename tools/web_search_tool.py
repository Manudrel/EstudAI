from langchain.tools import tool
from ddgs import DDGS


@tool
def web_search(query: str) -> str:
    """
    Pesquisa informações na web.
    """

    try:

        results = []

        with DDGS() as ddgs:

            for r in ddgs.text(
                query,
                max_results=5
            ):

                results.append(
                    f"""
                        Fonte: {r.get('title')}

                        Resumo:
                        {r.get('body')}

                        Link:
                        {r.get('href')}
                        """
                )

        return "\n\n".join(results)

    except Exception as e:
        return str(e)

if __name__ == "__main__":

    resultado = web_search.invoke(
        {
            "query": "Spring Boot"
        }
    )

    print(resultado)