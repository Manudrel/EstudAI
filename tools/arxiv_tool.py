from langchain.tools import tool
import arxiv


@tool
def search_arxiv(query: str) -> str:
    """
    Busca artigos científicos no ArXiv.
    """

    try:

        client = arxiv.Client()

        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []

        for paper in client.results(search):

            results.append(
                f"""
                Título: {paper.title}

                Autores: {', '.join(a.name for a in paper.authors)}

                Resumo:
                {paper.summary[:1000]}

                PDF:
                {paper.pdf_url}

                URL:
                {paper.entry_id}
                """
            )

        return "\n\n".join(results)

    except Exception as e:
        return f"Erro ao buscar artigos: {e}"


if __name__ == "__main__":
    print(
    search_arxiv.invoke(
        {"query": "Attention Is All You Need"}
        )
    )