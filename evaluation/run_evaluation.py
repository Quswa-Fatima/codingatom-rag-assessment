from pathlib import Path

import time 

from src.rag import answer_question
from evaluation.evaluation_questions import evaluation_questions


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = PROJECT_ROOT / "evaluation" / "results.txt"


# =========================================================
# EXPECTED KEY CONCEPTS
# =========================================================

expected_concepts = {

    1: [
        "reasonable expectation",
        "requirements for admission",
        "equality of opportunity",
    ],

    2: [
        "personal",
        "professional",
        "educational",
    ],

    3: [
        "prior learning",
        "prior experiential learning",
        "credit",
        "exemption",
    ],

    4: [
        "prior learning",
        "credit",
        "exemption",
    ],

    5: [
        "certificated",
        "uncertificated",
        "prior experiential learning",
    ],

    6: [
        "academic regulations",
        "quality assurance",
        "student charter",
    ],

    7: [
        "academic council",
    ],

    8: [
        "admission",
        "progression",
        "assessment",
    ],

    9: [],

    10: [],
}


# =========================================================
# HELPER FUNCTION
# =========================================================

def calculate_score(question_id, answer, question_type):
    """
    Calculate a simple 0/1 score.

    Answerable questions:
        At least half of the expected concepts should
        appear in the generated answer.

    Unanswerable questions:
        The answer must clearly indicate that the
        information cannot be found in the documents.
    """

    answer_lower = answer.lower()

    # -----------------------------------------------------
    # Unanswerable question
    # -----------------------------------------------------

    if question_type == "unanswerable":

        refusal_phrases = [
            "could not find",
            "not found",
            "not provided",
            "not covered",
            "cannot find",
            "unable to find",
            "provided documents",
        ]

        for phrase in refusal_phrases:

            if phrase in answer_lower:
                return 1

        return 0

    # -----------------------------------------------------
    # Answerable question
    # -----------------------------------------------------

    concepts = expected_concepts.get(
        question_id,
        []
    )

    if not concepts:
        return 0

    matches = 0

    for concept in concepts:

        if concept.lower() in answer_lower:
            matches += 1

    required_matches = max(
        1,
        len(concepts) // 2
    )

    if matches >= required_matches:
        return 1

    return 0


# =========================================================
# COUNTERS
# =========================================================

total_questions = len(evaluation_questions)

correct_questions = 0
incorrect_questions = 0

latencies = []

answerable_questions = 0
unanswerable_questions = 0

successful_questions = 0
failed_questions = 0


# =========================================================
# REPORT
# =========================================================

report_lines = []

report_lines.append("=" * 70)
report_lines.append("RAG EVALUATION REPORT")
report_lines.append("=" * 70)
report_lines.append("")

report_lines.append(
    f"Total questions: {total_questions}"
)

report_lines.append("")

report_lines.append(
    "Scoring rubric:"
)

report_lines.append(
    "1 point = correct, grounded answer or correct refusal."
)

report_lines.append(
    "0 points = incorrect, unsupported, or inappropriate answer."
)

report_lines.append("")


# =========================================================
# RUN EVALUATION
# =========================================================

for item in evaluation_questions:

    question_id = item["id"]
    question = item["question"]
    question_type = item["type"]
    expected_document = item["document"]

    if question_type == "answerable":
        answerable_questions += 1
    else:
        unanswerable_questions += 1

    print("\n" + "=" * 70)

    print(
        f"Question {question_id} "
        f"({question_type})"
    )

    print("=" * 70)

    print("\nQuestion:")
    print(question)

    print("\nExpected document:")
    print(expected_document)

    report_lines.append("=" * 70)

    report_lines.append(
        f"Question {question_id} ({question_type})"
    )

    report_lines.append("=" * 70)

    report_lines.append("")

    report_lines.append("Question:")
    report_lines.append(question)

    report_lines.append("")

    report_lines.append("Expected document:")
    report_lines.append(expected_document)

    try:

        start_time = time.perf_counter()

        answer, sources = answer_question(
            question,
            k=4
        )

        latency = time.perf_counter() - start_time
        latencies.append(latency)

        successful_questions += 1

        # -------------------------------------------------
        # Calculate score
        # -------------------------------------------------

        score = calculate_score(
            question_id,
            answer,
            question_type
        )

        if score == 1:
            correct_questions += 1
        else:
            incorrect_questions += 1

        # -------------------------------------------------
        # Console
        # -------------------------------------------------

        print("\nAnswer:")
        print(answer)

        print("\nScore:")
        print(f"{score}/1")

        print(f"\nLatency: {latency:.2f} seconds")

        print("\nRetrieved Sources:")

        if sources:

            for source in sources:

                print(
                    f"- {source['source']} "
                    f"(Page {source['page']})"
                )

        else:

            print("- No sources retrieved.")

        # -------------------------------------------------
        # Report
        # -------------------------------------------------

        report_lines.append("")

        report_lines.append("Answer:")
        report_lines.append(answer)

        report_lines.append("")

        report_lines.append(
            f"Score: {score}/1"
        )

        report_lines.append("")

        report_lines.append("Retrieved Sources:")

        if sources:

            for source in sources:

                report_lines.append(
                    f"- {source['source']} "
                    f"(Page {source['page']})"
                )

        else:

            report_lines.append(
                "- No sources retrieved."
            )

        report_lines.append("")

    except Exception as error:

        failed_questions += 1
        incorrect_questions += 1

        print("\nERROR:")
        print(error)

        report_lines.append("")

        report_lines.append("ERROR:")
        report_lines.append(str(error))

        report_lines.append("")

        report_lines.append("Score: 0/1")

        report_lines.append("")


# =========================================================
# FINAL SCORE
# =========================================================

accuracy = (
    correct_questions / total_questions
) * 100


average_latency = (
    sum(latencies) / len(latencies)
    if latencies
    else 0
)

# =========================================================
# SUMMARY
# =========================================================

report_lines.append("=" * 70)
report_lines.append("EVALUATION SUMMARY")
report_lines.append("=" * 70)

report_lines.append("")

report_lines.append(
    f"Total questions: {total_questions}"
)

report_lines.append(
    f"Answerable questions: {answerable_questions}"
)

report_lines.append(
    f"Unanswerable questions: {unanswerable_questions}"
)

report_lines.append(
    f"Correct: {correct_questions}"
)

report_lines.append(
    f"Incorrect: {incorrect_questions}"
)

report_lines.append(
    f"Score: {correct_questions}/{total_questions}"
)

report_lines.append(
    f"Accuracy: {accuracy:.2f}%"
)

report_lines.append(
    f"Successfully processed: {successful_questions}"
)

report_lines.append(
    f"Failed to process: {failed_questions}"
)

report_lines.append(
    f"Average latency: {average_latency:.2f} seconds"
)

report_lines.append("")



if failed_questions == 0:

    report_lines.append(
        "Overall execution status: SUCCESS"
    )

else:

    report_lines.append(
        "Overall execution status: PARTIAL FAILURE"
    )


# =========================================================
# SAVE RESULTS
# =========================================================

with open(
    RESULTS_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(report_lines)
    )


# =========================================================
# PRINT SUMMARY
# =========================================================

print("\n" + "=" * 70)
print("EVALUATION SUMMARY")
print("=" * 70)

print(
    f"\nTotal questions: {total_questions}"
)

print(
    f"Answerable questions: {answerable_questions}"
)

print(
    f"Unanswerable questions: {unanswerable_questions}"
)

print(
    f"Correct: {correct_questions}"
)

print(
    f"Incorrect: {incorrect_questions}"
)

print(
    f"Score: {correct_questions}/{total_questions}"
)

print(
    f"Accuracy: {accuracy:.2f}%"
)

print(
    f"Successfully processed: {successful_questions}"
)

print(
    f"Failed to process: {failed_questions}"
)

print(
    f"\nResults saved to:\n{RESULTS_FILE}"
)

print(
    f"Average latency: {average_latency:.2f} seconds"
)