from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Find the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Location of our PDF documents
DATA_DIR = PROJECT_ROOT / "data"


def load_documents():
    """Load all PDF documents from the data folder."""

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("ERROR: No PDF files found in the data folder.")
        return []

    all_documents = []

    print("=" * 60)
    print("STEP 1: PDF DOCUMENT LOADING")
    print("=" * 60)

    for pdf_file in pdf_files:
        print(f"\nLoading: {pdf_file.name}")

        try:
            loader = PyPDFLoader(str(pdf_file))
            documents = loader.load()

            print(f"Pages loaded: {len(documents)}")

            # Store the filename as metadata
            for document in documents:
                document.metadata["source_file"] = pdf_file.name

            all_documents.extend(documents)

            print("Status: SUCCESS")

        except Exception as error:
            print("Status: FAILED")
            print(f"Error: {error}")

    print("\n" + "=" * 60)
    print(f"Total pages loaded: {len(all_documents)}")
    print("=" * 60)

    return all_documents


def split_documents(documents):
    """Split documents into smaller chunks."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)

    print("\n" + "=" * 60)
    print("STEP 2: DOCUMENT CHUNKING")
    print("=" * 60)

    print(f"Original pages: {len(documents)}")
    print(f"Generated chunks: {len(chunks)}")

    # Add a unique chunk ID
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index

    print("\nExample chunk:")
    print("-" * 60)
    print(chunks[0].page_content[:1000])
    print("-" * 60)

    print("\nExample metadata:")
    print(chunks[0].metadata)

    return chunks


if __name__ == "__main__":

    # Step 1: Load PDFs
    documents = load_documents()

    if not documents:
        raise SystemExit("No documents were loaded.")

    # Step 2: Split PDFs into chunks
    chunks = split_documents(documents)

    print("\n" + "=" * 60)
    print("INGESTION + CHUNKING COMPLETED SUCCESSFULLY")
    print("=" * 60)