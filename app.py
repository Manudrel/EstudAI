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
### Sistema Multiagente

🔎 **Researcher**

- Pesquisa científica
- Busca em artigos
- Busca na Web

🧐 **Reviewer**

- Revisão técnica
- Organização
- Validação

👨‍🏫 **Professor**

- Planejamento pedagógico
- Material de estudo
- Exercícios
"""
    )

    st.divider()

    st.info(
        """
O EstudAI utiliza agentes especializados
para transformar um tema em um material
de estudo completo.
"""
    )


# =====================================
# HEADER
# =====================================

st.title("📚 EstudAI")

st.write(
    """
Digite qualquer tema e o sistema irá pesquisar,
revisar e gerar um material completo de estudo.
"""
)

topic = st.text_input(
    "Tema",
    value=st.session_state.topic,
    placeholder="Ex.: Attention Is All You Need"
)

# =====================================
# EXECUÇÃO
# =====================================

if st.button(
    "🚀 Gerar Material",
    use_container_width=True
):

    if topic.strip():

        st.session_state.topic = topic

        orchestrator = StudyOrchestrator()

        with st.spinner(
            "Os agentes estão trabalhando..."
        ):

            st.session_state.result = (
                orchestrator.execute(topic)
            )

# =====================================
# RESULTADOS
# =====================================

if st.session_state.result:

    result = st.session_state.result

    lesson = result["lesson"]

    # -------------------------
    # MÉTRICAS
    # -------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Conceitos",
            len(lesson.concepts)
        )

    with col2:
        st.metric(
            "Exercícios",
            len(lesson.exercises)
        )

    with col3:
        st.metric(
            "Resumo",
            len(lesson.summary_points)
        )

    st.divider()

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

        st.header("📘 Introdução")
        st.write(lesson.introduction)

        st.divider()

        st.header("📚 Conceitos Fundamentais")

        for index, concept in enumerate(
            lesson.concepts,
            start=1
        ):

            with st.container(border=True):

                st.subheader(
                    f"{index}. {concept.name}"
                )

                st.markdown(
                    "**Definição**"
                )

                st.write(
                    concept.definition
                )

                st.markdown(
                    "**Explicação**"
                )

                st.write(
                    concept.explanation
                )

                st.info(
                    f"**Exemplo**\n\n{concept.example}"
                )

        st.divider()

        st.header("💡 Analogia")

        st.info(
            lesson.analogy
        )

        st.divider()

        st.header("🌎 Aplicações Práticas")

        st.write(
            lesson.applications
        )

        st.divider()

        st.header("🎯 Dica do Professor")

        st.success(
            lesson.tip
        )

        st.divider()

        st.header("📝 Resumo")

        for point in lesson.summary_points:

            st.markdown(
                f"- {point}"
            )
    # =====================================
    # EXERCÍCIOS
    # =====================================

    with tabs[1]:

        st.header("📝 Exercícios de Fixação")

        exercise_tabs = st.tabs(
            [
                "📄 Questões",
                "✅ Gabarito"
            ]
        )

        # -----------------------------
        # QUESTÕES
        # -----------------------------

        with exercise_tabs[0]:

            st.info(
                "Tente resolver as questões antes de consultar o gabarito."
            )

            for i, exercise in enumerate(
                lesson.exercises,
                start=1
            ):

                difficulty = (
                    exercise.difficulty.lower()
                )

                if difficulty == "easy":
                    emoji = "🟢"
                    label = "Fácil"

                elif difficulty == "medium":
                    emoji = "🟡"
                    label = "Médio"

                else:
                    emoji = "🔴"
                    label = "Difícil"

                with st.container(border=True):

                    st.subheader(
                        f"{emoji} Questão {i}"
                    )

                    st.caption(
                        f"Dificuldade: {label}"
                    )

                    st.write(
                        exercise.question
                    )

                    st.text_area(
                        "Sua resposta (opcional)",
                        key=f"user_answer_{i}",
                        height=120,
                        placeholder="Digite sua resposta aqui..."
                    )

        # -----------------------------
        # GABARITO
        # -----------------------------

        with exercise_tabs[1]:

            st.warning(
                "Consulte o gabarito somente após tentar resolver as questões."
            )

            for i, exercise in enumerate(
                lesson.exercises,
                start=1
            ):

                difficulty = (
                    exercise.difficulty.lower()
                )

                if difficulty == "easy":
                    emoji = "🟢"
                    label = "Fácil"

                elif difficulty == "medium":
                    emoji = "🟡"
                    label = "Médio"

                else:
                    emoji = "🔴"
                    label = "Difícil"

                with st.expander(
                    f"{emoji} Questão {i} ({label})"
                ):

                    st.markdown(
                        "### Pergunta"
                    )

                    st.write(
                        exercise.question
                    )

                    st.markdown(
                        "### Resposta"
                    )

                    st.success(
                        exercise.answer
                    )
    # =====================================
    # PESQUISA
    # =====================================

    with tabs[2]:

        research = result["research"]

        st.header("🔎 Relatório de Pesquisa")

        st.info(
            "Este relatório foi produzido pelo agente Researcher e serviu como base para os demais agentes."
        )

        st.markdown(research.report)

        st.divider()

        # =====================================
        # DOWNLOADS
        # =====================================

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                label="📥 Baixar Markdown",
                data=research.report,
                file_name=(
                    f"{st.session_state.topic}_pesquisa.md"
                ),
                mime="text/markdown",
                use_container_width=True
            )

        with col2:

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
                mime="application/pdf",
                use_container_width=True
            )

        st.divider()

        # =====================================
        # ETAPAS DA PESQUISA
        # =====================================

        st.header("🛠 Histórico da Pesquisa")

        st.caption(
            "Ferramentas utilizadas pelo agente Researcher durante a investigação."
        )

        if research.research_steps:

            for index, step in enumerate(
                research.research_steps,
                start=1
            ):

                with st.expander(
                    f"{index}. {step.tool}"
                ):

                    col1, col2 = st.columns(
                        [1, 3]
                    )

                    with col1:

                        st.markdown(
                            "**Ferramenta**"
                        )

                        st.code(
                            step.tool
                        )

                    with col2:

                        st.markdown(
                            "**Parâmetros**"
                        )

                        st.json(
                            step.args
                        )

                    st.markdown(
                        "**Resultado Obtido**"
                    )

                    st.text_area(
                        label="",
                        value=step.result,
                        height=250,
                        disabled=True,
                        key=f"tool_result_{index}"
                    )

        else:

            st.success(
                "Nenhuma ferramenta foi utilizada nesta pesquisa."
            )

        st.divider()

        st.success(
            "✅ Fluxo concluído com sucesso!\n\n"
            "Researcher → Reviewer → Professor"
        )