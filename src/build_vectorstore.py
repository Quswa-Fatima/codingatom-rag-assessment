from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from ingest import load_documents, split_documents


# Find the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Where the FAISS database will be saved
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"


def create_embeddings():
    """Create the local embedding model."""

    print("\n" + "=" * 60)
    print("STEP 3: LOADING EMBEDDING MODEL")
    print("=" * 60)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding model loaded successfully.")

    return embeddings


def build_vectorstore(chunks, embeddings):
    """Convert chunks into vectors and save them in FAISS."""

    print("\n" + "=" * 60)
    print("STEP 4: BUILDING FAISS VECTOR STORE")
    print("=" * 60)

    print(f"Chunks to embed: {len(chunks)}")

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    VECTORSTORE_DIR.mkdir(exist_ok=True)

    vectorstore.save_local(str(VECTORSTORE_DIR))

    print(f"FAISS vector store saved to:")
    print(VECTORSTORE_DIR)

    return vectorstore


if __name__ == "__main__":

    # 1. Load PDF pages
    documents = load_documents()

    if not documents:
        raise SystemExit("No documents were loaded.")

    # 2. Split pages into chunks
    chunks = split_documents(documents)

    if not chunks:
        raise SystemExit("No chunks were created.")

    # 3. Load embedding model
    embeddings = create_embeddings()

    # 4. Build and save FAISS
    vectorstore = build_vectorstore(
        chunks,
        embeddings
    )

    print("\n" + "=" * 60)
    print("VECTOR STORE CREATED SUCCESSFULLY")
    print("=" * 60)