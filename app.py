import streamlit as st

from services.orchestrator import (
    StudyOrchestrator
)

st.set_page_config(
    page_title="EstudAI",
    page_icon="📚",
    layout="wide"
)

with st.sidebar:

    st.title("EstudAI")

    st.markdown(
        """
        ### Agentes

        🔎 Researcher

        🧐 Reviewer

        👨‍🏫 Professor
        """
    )

st.title("📚 EstudAI")

st.write(
    "Sistema Multiagente para geração de material de estudo."
)

topic = st.text_input(
    "Digite um tema"
)

if st.button("Gerar Material"):

    orchestrator = StudyOrchestrator()

    with st.spinner(
        "Executando agentes..."
    ):
        result = orchestrator.execute(
            topic
        )

    lesson = result["lesson"]

    tabs = st.tabs(
        [
            "📖 Aula",
            "📝 Exercícios",
            "🔎 Pesquisa"
        ]
    )

    with tabs[0]:

        st.header(
            lesson.title
        )

        st.subheader(
            "Introdução"
        )

        st.write(
            lesson.introduction
        )

        st.subheader(
            "Conceito"
        )

        st.write(
            lesson.explanation
        )

        st.subheader(
            "Analogia"
        )

        st.info(
            lesson.analogy
        )

        st.subheader(
            "Aplicações"
        )

        st.write(
            lesson.applications
        )

        st.subheader(
            "Dica do Professor"
        )

        st.success(
            lesson.tip
        )

    with tabs[1]:

        for exercise in (
            lesson.exercises
        ):

            st.markdown(
                f"### {exercise.difficulty.upper()}"
            )

            st.write(
                exercise.question
            )

            with st.expander(
                "Ver Resposta"
            ):

                st.write(
                    exercise.answer
                )

    with tabs[2]:

        research = result["research"]

        st.subheader(
            "Relatório"
        )

        st.write(
            research.report
        )

        st.subheader(
            "Etapas da Pesquisa"
        )

        for step in (
            research.research_steps
        ):

            with st.expander(
                step.tool
            ):

                st.json(
                    {
                        "args": step.args,
                        "result": step.result
                    }
                )