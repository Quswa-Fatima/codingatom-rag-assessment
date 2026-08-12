from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


# ---------------------------------------------------------
# 1. PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"


# ---------------------------------------------------------
# 2. LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# 3. LOAD EMBEDDING MODEL
# ---------------------------------------------------------

def load_embeddings():
    """Load the same embedding model used to build FAISS."""

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings


# ---------------------------------------------------------
# 4. LOAD FAISS VECTOR STORE
# ---------------------------------------------------------

def load_vectorstore():
    """Load the saved FAISS vector database."""

    embeddings = load_embeddings()

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


# ---------------------------------------------------------
# 5. CREATE GROQ LLM
# ---------------------------------------------------------

def create_llm():
    """Create the Groq language model."""

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
    )

    return llm


# ---------------------------------------------------------
# 6. CREATE RAG PROMPT
# ---------------------------------------------------------

def create_prompt():
    """Create the prompt used by the RAG system."""

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful question-answering assistant.

You must answer the user's question using ONLY the
information provided in the context below.

Do not use outside knowledge.

If the answer cannot be found in the provided context,
clearly say:

"I could not find the answer in the provided documents."

Do not invent facts, regulations, policies, dates, or
requirements.

Answer the question clearly and concisely.

Do not provide a separate Sources section.
The application will add citations automatically.

Context:
{context}

Question:
{question}
"""
    )

    return prompt


# ---------------------------------------------------------
# 7. FORMAT RETRIEVED DOCUMENTS
# ---------------------------------------------------------

def format_context(documents):
    """Convert retrieved documents into prompt context."""

    context_parts = []

    for document in documents:

        source = document.metadata.get(
            "source_file",
            "Unknown source"
        )

        page = document.metadata.get(
            "page",
            0
        ) + 1

        text = document.page_content

        context_parts.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{text}"
        )

    return "\n\n---\n\n".join(context_parts)


# ---------------------------------------------------------
# 8. ASK A QUESTION
# ---------------------------------------------------------
def answer_question(question, k=4):
    """Retrieve relevant chunks and generate an answer."""

    # Load FAISS
    vectorstore = load_vectorstore()

    # Retrieve relevant chunks with similarity scores
    results = vectorstore.similarity_search_with_score(
        question,
        k=k
    )

    # Keep only sufficiently relevant documents.
    # Lower FAISS distance means greater similarity.
    SIMILARITY_THRESHOLD = 1.2

    documents = [
        document
        for document, score in results
        if score <= SIMILARITY_THRESHOLD
    ]

    if not documents:

        return (
            "I could not find the answer in the provided documents.",
            []
        )

    # Format context for the LLM
    context = format_context(documents)

    # Create prompt
    prompt = create_prompt()

    # Create LLM
    llm = create_llm()

    # Build final prompt
    messages = prompt.format_messages(
        context=context,
        question=question
    )

    # Generate answer
    response = llm.invoke(messages)

    # Build citations from actual retrieved documents
    sources = []

    for document in documents:

        source = document.metadata.get(
            "source_file",
            "Unknown source"
        )

        page = document.metadata.get(
            "page",
            0
        ) + 1

        citation = {
            "source": source,
            "page": page
        }

        if citation not in sources:
            sources.append(citation)

    return response.content, sources

# ---------------------------------------------------------
# 9. COMMAND-LINE INTERFACE
# ---------------------------------------------------------
if __name__ == "__main__":

    print("=" * 60)
    print("CODINGATOM RAG QUESTION ANSWERING SYSTEM")
    print("=" * 60)

    question = input("\nEnter your question: ")

    print("\nGenerating answer...\n")

    answer, sources = answer_question(question)

    print("=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(answer)

    print("\n" + "=" * 60)
    print("RETRIEVED SOURCES")
    print("=" * 60)

    for source in sources:
        print(
            f"- {source['source']}, "
            f"Page {source['page']}"
        )