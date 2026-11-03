"""Evaluate local copilot retrieval against expected source labels."""
import argparse
import json
from pathlib import Path

from copilot_retrieval import KnowledgeBase

ROOT = Path(__file__).resolve().parent
DEFAULT_CASES = ROOT / "evaluation" / "retrieval_cases.json"


def evaluate(cases: list[dict], knowledge_base: KnowledgeBase, top_k: int) -> dict:
    recall_scores: list[float] = []
    reciprocal_ranks: list[float] = []
    rows: list[dict] = []

    for case in cases:
        expected = set(case["expected_sources"])
        results = knowledge_base.search(case["question"], limit=top_k)
        retrieved = [item["source"] for item in results]
        hits = expected.intersection(retrieved)
        if expected:
            recall_scores.append(len(hits) / len(expected))
            first_rank = next((rank for rank, source in enumerate(retrieved, start=1) if source in expected), None)
            reciprocal_ranks.append(1 / first_rank if first_rank else 0.0)

        rows.append({
            "question": case["question"],
            "expected": sorted(expected),
            "retrieved": retrieved,
            "hit": bool(hits),
        })

    return {
        "case_count": len(cases),
        "top_k": top_k,
        "recall_at_k": sum(recall_scores) / len(recall_scores) if recall_scores else 0.0,
        "mrr": sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure whether the copilot retrieves expected source documents.")
    parser.add_argument("--top-k", type=int, default=3, help="Number of retrieved chunks to inspect (default: 3).")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES, help="Path to a JSON evaluation case file.")
    args = parser.parse_args()
    if args.top_k < 1:
        parser.error("--top-k must be at least 1")

    cases = json.loads(args.cases.read_text(encoding="utf-8-sig"))
    knowledge_base = KnowledgeBase(ROOT / "knowledge")
    result = evaluate(cases, knowledge_base, args.top_k)

    print(f"Cases: {result['case_count']}")
    print(f"Recall@{result['top_k']}: {result['recall_at_k']:.3f}")
    print(f"MRR: {result['mrr']:.3f}")
    print("\nPer-question retrieval:")
    for row in result["rows"]:
        mark = "PASS" if row["hit"] else "MISS"
        print(f"[{mark}] {row['question']}")
        print(f"  expected: {', '.join(row['expected']) or '(none)'}")
        print(f"  retrieved: {', '.join(row['retrieved']) or '(none)'}")


if __name__ == "__main__":
    main()
