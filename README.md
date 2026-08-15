# University Academic Regulations RAG System

A Retrieval-Augmented Generation (RAG) application for answering questions about the University of Westminster 2025–26 academic regulations.

The system retrieves relevant information from the provided PDF documents and uses a Large Language Model (LLM) to generate grounded answers with source references.

---

## 1. Project Overview

This project implements a document-based RAG pipeline that allows users to ask questions about University academic regulations.

The system:

- Loads academic regulation PDFs
- Splits documents into smaller text chunks
- Generates embeddings for the chunks
- Stores embeddings in a FAISS vector database
- Retrieves relevant document sections for a user query
- Uses the Groq LLM to generate an answer
- Displays the answer along with source documents and page numbers
- Handles questions for which relevant information cannot be found

The application is provided through a Streamlit web interface.

---

## 2. Documents Used

The RAG system uses the following four PDF documents:

1. `Academic-regs-2025-26-Section-1-Introduction.pdf`
2. `Academic-regs-2025-26-Section-2-Statutes-and-principles.pdf`
3. `Academic-regs-2025-26-Section-3-Admissions-regulations-for-taught-courses.pdf`
4. `Academic-regs-2025-26-Section-4-Recognition-of-Prior-Learning-(RPL)-regulations.pdf`

The documents contain academic regulations relating to areas such as admissions, statutes and principles, and Recognition of Prior Learning.

---

## 3. RAG Architecture

The implemented pipeline follows these stages:

```text
PDF Documents
      |
      v
Document Loading
      |
      v
Text Chunking
      |
      v
Sentence Embeddings
      |
      v
FAISS Vector Store
      |
      v
Similarity Retrieval
      |
      v
Relevant Context
      |
      v
Groq LLM
      |
      v
Grounded Answer + Sources

4. Technologies Used
Python
LangChain
LangChain Community
LangChain Text Splitters
Hugging Face Sentence Transformers
FAISS
Groq API
Streamlit
PyPDF
python-dotenv


5. Document Processing

The four supplied PDF documents contain a total of:

20 original pages
77 generated text chunks

The documents are loaded using a PDF document loader and divided into smaller chunks before generating embeddings.

The resulting embeddings are stored in a FAISS vector store to enable semantic similarity search.

6. Retrieval and Grounded Answers

When a user submits a question, the system:

Converts the question into an embedding.
Searches the FAISS vector store.
Retrieves the most relevant document chunks.
Applies a similarity threshold to reduce irrelevant retrievals.
Passes relevant context to the LLM.
Generates an answer based on the retrieved documents.
Displays the source PDF and page number.

This allows the generated answer to be traced back to the supplied academic regulations.

## 7. Language Model

The application uses:

`openai/gpt-oss-20b`

through the Groq API.

The Groq API key is stored in an environment variable and is not hard-coded into the application.

The model was selected as the replacement for the previously used `llama-3.1-8b-instant` model, which was scheduled for decommissioning.

8. Installation

Create a virtual environment

On Windows PowerShell:

python -m venv venv

Activate the environment:

.\venv\Scripts\Activate.ps1
Install dependencies
pip install -r requirements.txt


9. Environment Configuration

Create a .env file in the project root:

GROQ_API_KEY=your_actual_groq_api_key

A .env.example file is provided as a template.

The actual .env file should not be uploaded to GitHub or included in the final submission.

10. Running the Application

From the project root, run:

streamlit run app.py

The Streamlit application will be available at:

http://localhost:8501
Example questions
What are the principles of admission to taught courses?
What is Recognition of Prior Learning?
What do course regulations include?

The application also includes example questions through the Streamlit interface.

## 11. Evaluation

The project contains a 10-question evaluation set:

- 8 answerable questions
- 2 deliberately unanswerable questions

The scoring rubric is:

- 1 point: Correct, grounded answer or correct refusal for an unanswerable question
- 0 points: Incorrect, unsupported, or inappropriate answer

### Evaluation Results

Total questions: 10
Answerable questions: 8
Unanswerable questions: 2
Correct: 10
Incorrect: 0
Score: 10/10
Accuracy: 100.00%
Successfully processed: 10
Failed to process: 0


The evaluation results are saved in:

`evaluation/results.txt`

Average latency: **10.64 seconds per request**

Run the evaluation:

```bash
python -m evaluation.run_evaluation


## 12. Latency

The measured average end-to-end latency across the 10-question evaluation was:

**10.64 seconds per request**

This is the measured evaluation-pipeline latency and should not be interpreted as LLM-only inference time.

Actual latency can vary depending on model loading, network conditions, retrieval, query length, and API response time.

## 13. Estimated Cost

The project uses the Groq `openai/gpt-oss-20b` model.

A rough estimated cost depends on the number of input and output tokens used for each request.

Actual cost varies depending on token usage and the applicable Groq API pricing.

The previous cost estimate was based on the retired `llama-3.1-8b-instant` model and is therefore not used as the final estimate for the updated system.

14. Failure Cases
Failure Case 1 — Out-of-Scope Query

Example:

What is the weather today?

The supplied academic-regulation documents do not contain weather information.

The system is designed to indicate that the answer cannot be found in the provided documents rather than generating an unsupported answer.

Failure Case 2 — Retrieval Threshold Sensitivity

During testing, the question:

What is Recognition of Prior Learning?

initially returned no relevant sources when the similarity threshold was too strict.

The retrieval threshold was adjusted after testing, allowing relevant RPL content to be retrieved.

Proposed Improvements

Future retrieval improvements could include:

Threshold tuning using a larger validation dataset
Retrieval reranking
Hybrid keyword and semantic search
Adaptive confidence thresholds

Detailed failure-case documentation is available in:

evaluation/failure_cases.md


15. Security Considerations

Important security considerations for the application include:

Protecting the Groq API key using environment variables
Excluding .env from the project submission
Handling out-of-scope questions
Considering prompt-injection risks in retrieved documents
Managing retrieval false negatives
Monitoring third-party dependency risks

Detailed security documentation is available in:

evaluation/security.md


16. Project Structure
codingatom-rag-assessment/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── Academic regulation PDF documents
│
├── evaluation/
│   ├── evaluation_questions.py
│   ├── run_evaluation.py
│   ├── results.txt
│   ├── failure_cases.md
│   └── security.md
│
├── screenshots/
│   ├── 01_streamlit_interface.png
│   ├── 02_admissions_answer.png
│   ├── 03_rpl_answer.png
│   ├── 04_out_of_scope.png
│   ├── 05_document_loading.png
│   ├── 06_chunking.png
│   └── 07_evaluation_summary.png
│
├── src/
│   ├── __init__.py
│   ├── build_vectorstore.py
│   ├── ingest.py
│   ├── rag.py
│   ├── retrieve.py
│   └── test_groq.py
│
└── vectorstore/
    └── FAISS vector database files


17. Limitations

This project is an academic prototype rather than a production system.

The main limitations are:

The system depends on the supplied document collection.
Questions outside the document collection cannot be reliably answered.
The evaluation dataset contains only 10 questions.
The scoring rubric is concept-based rather than a full semantic or LLM-judge evaluation.
Latency can vary depending on network and API conditions.
The estimated cost is based on assumed token usage.


18. Future Improvements

Potential improvements include:

Expanding the evaluation dataset
Adding automated semantic evaluation
Implementing retrieval reranking
Using hybrid keyword and semantic retrieval
Improving adaptive retrieval thresholds
Adding stronger prompt-injection protection
Tracking token usage and actual request costs
Improving latency
Adding authentication and rate limiting
Adding production monitoring and logging


19. Author

Name: QUSWA FATIMA

