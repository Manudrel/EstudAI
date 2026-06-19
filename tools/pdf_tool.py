from langchain.tools import tool
from pypdf import PdfReader


@tool
def read_pdf(pdf_path: str) -> str:
    """
    Lê um arquivo PDF e retorna seu conteúdo textual.
    """

    try:
        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text[:10000]

    except Exception as e:
        return f"Erro ao ler PDF: {str(e)}"