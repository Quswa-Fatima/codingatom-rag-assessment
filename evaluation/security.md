# Security and Vulnerability Assessment

## 1. API Key Exposure

### Risk
The Groq API key is required by the application and is stored in an environment variable.

If the key were hard-coded into source code or committed to a public repository, it could be exposed and misused.

### Mitigation
The API key is stored in `.env` and loaded using environment variables. The `.env` file is excluded from the project submission through `.gitignore`.

A `.env.example` file is provided containing only a placeholder.

Example:

GROQ_API_KEY=your_groq_api_key_here

The actual API key is never included in the source code or documentation.

---

## 2. Prompt Injection Through Retrieved Documents

### Risk
A document used by a RAG system could contain text that attempts to manipulate the language model, for example by instructing it to ignore the original task or reveal sensitive information.

### Mitigation
The system restricts the knowledge source to the supplied University academic-regulation documents and uses retrieval to provide relevant context to the model.

For a production system, retrieved content should be clearly separated from system instructions and additional prompt-injection detection should be implemented.

---

## 3. Out-of-Scope / Hallucination Risk

### Risk
A language model may generate an answer even when the requested information is not present in the document collection.

### Evidence
The evaluation includes two deliberately unanswerable questions:

- What is the University cafeteria menu for today?
- What is the weather today?

The system is designed to return a response indicating that the information could not be found rather than inventing an answer.

### Mitigation
A retrieval similarity threshold is used so that low-confidence retrievals can be rejected before generating an answer.

---

## 4. Retrieval False Negatives

### Risk
A relevant document may fail to be retrieved when the similarity threshold is too strict.

### Evidence
During testing, the question:

"What is Recognition of Prior Learning?"

initially produced no retrieved sources even though the supplied RPL regulations contained relevant information.

### Mitigation
The retrieval threshold was adjusted after testing. For a production system, the threshold should be tuned using a representative validation dataset. A reranking stage could also improve retrieval quality.

---

## 5. Dependency and Supply-Chain Risk

### Risk
The application depends on external Python packages and third-party services. Vulnerabilities or breaking changes in dependencies could affect the application.

### Mitigation
The required Python packages are documented in `requirements.txt`. Dependencies should be regularly updated and tested before deployment.

---

## Security Limitations

This project is an academic prototype rather than a production security system.

The assessment focuses on demonstrating a functional RAG pipeline and identifying important security considerations. A production deployment would require additional controls such as authentication, rate limiting, structured prompt-injection defenses, dependency scanning, logging, monitoring, and secret-management infrastructure.