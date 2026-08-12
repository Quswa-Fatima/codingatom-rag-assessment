import streamlit as st

from src.rag import answer_question


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="University Regulations RAG",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 25px;
    }

    .source-box {
        padding: 12px 15px;
        border-radius: 8px;
        border: 1px solid #dddddd;
        margin-bottom: 8px;
        background-color: #fafafa;
    }

    .answer-box {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dddddd;
        background-color: #fafafa;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📚 About This Project")

    st.write(
        """
        This application uses **Retrieval-Augmented Generation (RAG)**
        to answer questions from the University of Westminster
        Academic Regulations 2025–26.
        """
    )

    st.divider()

    st.subheader("System Information")

    st.write("📄 **Documents:** 4")
    st.write("📑 **Pages:** 20")
    st.write("🧩 **Text chunks:** 77")
    st.write("🔎 **Retriever:** FAISS")
    st.write("🧠 **Embeddings:** MiniLM")
    st.write("🤖 **LLM:** Groq")

    st.divider()

    st.subheader("How it works")

    st.write(
        """
        1. User asks a question.
        2. FAISS retrieves relevant document chunks.
        3. Retrieved context is sent to the LLM.
        4. The LLM generates a grounded answer.
        5. Source documents and pages are displayed.
        """
    )

    st.divider()

    st.caption(
        "Academic Regulations RAG System"
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📚 University Regulations RAG</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Ask questions about the University of Westminster
    Academic Regulations 2025–26.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INFORMATION BOX
# =========================================================

st.info(
    "💡 Answers are generated using only the information "
    "retrieved from the provided academic regulation documents."
)


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.subheader("Example Questions")

example_questions = [
    "What are the principles of admission to taught courses?",
    "What is Recognition of Prior Learning (RPL)?",
    "What are the regulations for admission with credit or exemption?"
]

cols = st.columns(3)

for index, example in enumerate(example_questions):

    with cols[index]:

        if st.button(
            example,
            key=f"example_{index}",
            use_container_width=True
        ):

            st.session_state["question"] = example


# =========================================================
# QUESTION INPUT
# =========================================================

question = st.text_area(
    "Enter your question",
    value=st.session_state.get("question", ""),
    placeholder="Example: What are the principles of admission?",
    height=120
)


# =========================================================
# ASK QUESTION
# =========================================================

if st.button(
    "🔍 Ask Question",
    type="primary",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter a question before clicking Ask Question."
        )

    else:

        with st.spinner(
            "Searching the academic regulations and generating an answer..."
        ):

            try:

                answer, sources = answer_question(
                    question,
                    k=4
                )

                # =========================================
                # ANSWER SECTION
                # =========================================

                st.divider()

                st.subheader("💬 Answer")

                st.markdown(
                    f"""
                    <div class="answer-box">
                    {answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # =========================================
                # SOURCES SECTION
                # =========================================

                st.subheader("📖 Sources")

                if sources:

                    for source in sources:

                        st.markdown(
                            f"""
                            <div class="source-box">
                            📄 <strong>{source['source']}</strong>
                            &nbsp; — &nbsp;
                            Page <strong>{source['page']}</strong>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.write(
                        "No source information was retrieved."
                    )

                # =========================================
                # RETRIEVAL INFORMATION
                # =========================================

                st.caption(
                    f"Retrieved {len(sources)} source(s) "
                    f"from the document collection."
                )

            except Exception as error:

                st.error(
                    "An error occurred while processing your question."
                )

                st.exception(error)