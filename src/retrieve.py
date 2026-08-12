from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# Find the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Location of our saved FAISS database
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"


def load_vectorstore():
    """Load the previously created FAISS vector store."""

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def search_documents(query, k=4):
    """Retrieve the most relevant document chunks."""

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search_with_score(
        query,
        k=k
    )

    return results


if __name__ == "__main__":

    print("=" * 60)
    print("RAG RETRIEVAL TEST")
    print("=" * 60)

    query = input("\nEnter your question: ")

    results = search_documents(query, k=4)

    print("\n" + "=" * 60)
    print("RETRIEVED RESULTS")
    print("=" * 60)

    for rank, (document, score) in enumerate(results, start=1):

        print(f"\n--- Result {rank} ---")
        print(f"Similarity score: {score:.4f}")
        print(f"Source file: {document.metadata.get('source_file')}")
        print(f"Page: {document.metadata.get('page', 0) + 1}")

        print("\nContent:")
        print(document.page_content[:1500])