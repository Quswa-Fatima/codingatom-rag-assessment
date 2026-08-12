# Failure Cases and Improvements

## Failure Case 1: Out-of-Scope Query

### Query
What is the weather today?

### Observed Behavior
The question is outside the scope of the provided University academic regulations. The RAG system correctly returned a response indicating that the answer could not be found in the provided documents and did not use irrelevant retrieved sources.

### Limitation
The system is dependent on the document collection supplied during ingestion. Information that is not contained in these documents cannot be reliably answered.

### Proposed Improvement
An explicit out-of-domain classifier could be added before retrieval. This would allow clearly unrelated queries to be rejected earlier and reduce unnecessary retrieval and LLM calls.

---

## Failure Case 2: Retrieval Threshold Sensitivity

### Query
What is Recognition of Prior Learning?

### Observed Behavior
During testing, the system initially returned no retrieved sources for this question even though the supplied RPL regulations contained relevant information. The retrieval threshold was subsequently adjusted, after which the system successfully retrieved relevant RPL content and generated an answer.

### Limitation
A fixed similarity threshold can be too strict for some semantically relevant queries and may result in false negatives during retrieval.

### Proposed Improvement
The retrieval stage could be improved by tuning the threshold using a validation dataset, adding a reranking stage, or combining semantic similarity with keyword and metadata-based matching. Adaptive confidence thresholds could also be investigated.