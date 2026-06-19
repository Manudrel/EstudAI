from langchain.tools import tool
import arxiv


@tool
def search_arxiv(query: str) -> str:
    """
    Busca artigos científicos no ArXiv.
    """

    try:

        search = arxiv.Search(
            query=query,
            max_results=5
        )

        results = []

        for paper in search.results():

            results.append(
                f"""
Título: {paper.title}

Autores: {', '.join([a.name for a in paper.authors])}

Resumo:
{paper.summary[:1000]}

URL:
{paper.entry_id}
"""
            )

        return "\n\n".join(results)

    except Exception as e:
        return str(e)