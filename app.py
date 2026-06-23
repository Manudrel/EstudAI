import streamlit as st

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from services.orchestrator import (
    StudyOrchestrator
)

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="EstudAI",
    page_icon="📚",
    layout="wide"
)

# =====================================
# SESSION STATE
# =====================================

if "result" not in st.session_state:
    st.session_state.result = None

if "topic" not in st.session_state:
    st.session_state.topic = ""

# =====================================
# PDF
# =====================================

def create_pdf(title: str, content: str):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 12),
        Paragraph(
            content.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    ]

    doc.build(elements)

    buffer.seek(0)

    return buffer

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("📚 EstudAI")

    st.markdown(
        """
        ### Agentes

        🔎 Researcher

        🧐 Reviewer

        👨‍🏫 Professor
        """
    )

    st.divider()

    st.markdown(
        """
        Sistema Multiagente para geração
        automática de material de estudo.
        """
    )

# =====================================
# HEADER
# =====================================

st.title("📚 EstudAI")

st.write(
    """
    Gere aulas completas, exercícios e pesquisas
    utilizando agentes especializados.
    """
)

topic = st.text_input(
    "Digite um tema para estudar",
    value=st.session_state.topic
)

# =====================================
# EXECUÇÃO
# =====================================

if st.button("Gerar Material") and topic:

    st.session_state.topic = topic

    orchestrator = StudyOrchestrator()

    with st.spinner(
        "Executando agentes..."
    ):

        st.session_state.result = (
            orchestrator.execute(topic)
        )

# =====================================
# RESULTADO
# =====================================

if st.session_state.result:

    result = st.session_state.result

    lesson = result["lesson"]

    tabs = st.tabs(
        [
            "📖 Aula",
            "📝 Exercícios",
            "🔎 Pesquisa"
        ]
    )

    # =====================================
    # AULA
    # =====================================

    with tabs[0]:

        st.title(lesson.title)

        st.header("Introdução")
        st.write(lesson.introduction)

        if hasattr(lesson, "concepts"):

            st.header(
                "Conceitos Fundamentais"
            )

            for concept in lesson.concepts:

                st.subheader(
                    concept.name
                )

                st.markdown(
                    f"**Definição**\n\n{concept.definition}"
                )

                st.markdown(
                    f"**Explicação**\n\n{concept.explanation}"
                )

                st.info(
                    f"Exemplo:\n\n{concept.example}"
                )

        else:

            st.header("Explicação")
            st.write(
                lesson.explanation
            )

        st.header("Analogia")
        st.info(
            lesson.analogy
        )

        st.header(
            "Aplicações Práticas"
        )

        st.write(
            lesson.applications
        )

        st.header(
            "Dica do Professor"
        )

        st.success(
            lesson.tip
        )

        st.header(
            "Resumo"
        )

        for point in lesson.summary_points:

            st.markdown(
                f"- {point}"
            )

    # =====================================
    # EXERCÍCIOS
    # =====================================

    with tabs[1]:

        st.header(
            "Exercícios de Fixação"
        )

        for i, exercise in enumerate(
            lesson.exercises,
            start=1
        ):

            difficulty = (
                exercise.difficulty.upper()
            )

            with st.expander(
                f"Questão {i} ({difficulty})"
            ):

                st.markdown(
                    f"### Pergunta\n\n{exercise.question}"
                )

                st.markdown(
                    "### Resposta"
                )

                st.write(
                    exercise.answer
                )

    # =====================================
    # PESQUISA
    # =====================================

    with tabs[2]:

        research = result["research"]

        st.header(
            "Relatório de Pesquisa"
        )

        st.markdown(
            research.report
        )

        # -------------------------
        # Markdown
        # -------------------------

        st.download_button(
            label="📥 Baixar Markdown",
            data=research.report,
            file_name=(
                f"{st.session_state.topic}_pesquisa.md"
            ),
            mime="text/markdown"
        )

        # -------------------------
        # PDF
        # -------------------------

        pdf_file = create_pdf(
            f"Pesquisa - {st.session_state.topic}",
            research.report
        )

        st.download_button(
            label="📄 Baixar PDF",
            data=pdf_file,
            file_name=(
                f"{st.session_state.topic}_pesquisa.pdf"
            ),
            mime="application/pdf"
        )

        st.divider()

        st.header(
            "Etapas da Pesquisa"
        )

        for step in research.research_steps:

            with st.expander(
                f"🔧 {step.tool}"
            ):

                st.json(
                    {
                        "args": step.args,
                        "result": step.result
                    }
                )