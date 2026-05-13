#!/usr/bin/env python
"""Simple fallback RAGAS-like scoring using token overlap."""

import json
from pathlib import Path
from dotenv import load_dotenv

from vna_chatbot import load_config, load_pages, answer_question, retrieve_pages


def run_fallback_eval(dataset_path: Path, config_path: Path) -> None:
    """Run lightweight token-overlap based scoring without full RAGAS."""
    load_dotenv()
    config = load_config(config_path)
    pages = load_pages(config.data_path)
    
    # Load examples from JSONL
    examples = []
    for line in dataset_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            examples.append(json.loads(line))
    
    print(f"Loaded {len(examples)} examples from {dataset_path}")
    print("=" * 80)
    
    # Prepare rows by running chatbot on each question
    prepared_rows = []
    for i, example in enumerate(examples, 1):
        question = example.get("question", "")
        reference = example.get("reference", "")
        
        print(f"\n[{i}/{len(examples)}] Question: {question[:60]}...")
        result = answer_question(question, config, pages)
        retrieved_pages = retrieve_pages(question, pages, top_k=config.top_k)
        contexts = [page.get("body_text") or page.get("body_markdown") or "" for page in retrieved_pages]
        
        prepared_rows.append(
            {
                "question": question,
                "answer": result["answer"],
                "contexts": contexts,
                "ground_truth": reference,
            }
        )
    
    # Run fallback scoring
    print("\n" + "=" * 80)
    print("FALLBACK SCORING (Token Overlap Based)")
    print("=" * 80)
    
    scores = []
    for row in prepared_rows:
        answer = row.get("answer", "") or ""
        gt = (row.get("ground_truth") or "").lower()
        contexts = " ".join(row.get("contexts") or [])
        
        gt_tokens = set(gt.split())
        ans_tokens = set(answer.lower().split())
        ctx_tokens = set(contexts.lower().split())
        
        faithfulness = (len(gt_tokens & ans_tokens) / max(1, len(gt_tokens))) if gt_tokens else 0.0
        answer_relevancy_score = (len(ans_tokens & gt_tokens) / max(1, len(ans_tokens))) if ans_tokens else 0.0
        context_precision_score = (len(ans_tokens & ctx_tokens) / max(1, len(ans_tokens))) if ans_tokens else 0.0
        
        scores.append(
            {
                "question": row.get("question")[:50],
                "faithfulness": round(faithfulness, 3),
                "answer_relevancy": round(answer_relevancy_score, 3),
                "context_precision": round(context_precision_score, 3),
            }
        )
    
    # Print per-example scores
    print("\nPer-example scores:")
    for i, s in enumerate(scores, 1):
        print(f"  [{i}] {s['question']}... → f:{s['faithfulness']} ar:{s['answer_relevancy']} cp:{s['context_precision']}")
    
    # Aggregate
    avg = {"faithfulness": 0.0, "answer_relevancy": 0.0, "context_precision": 0.0}
    for s in scores:
        avg["faithfulness"] += s["faithfulness"]
        avg["answer_relevancy"] += s["answer_relevancy"]
        avg["context_precision"] += s["context_precision"]
    n = len(scores) or 1
    avg = {k: round(v / n, 3) for k, v in avg.items()}
    
    print("\n" + "=" * 80)
    print("AGGREGATED SCORES:")
    print(f"  faithfulness:     {avg['faithfulness']}")
    print(f"  answer_relevancy: {avg['answer_relevancy']}")
    print(f"  context_precision: {avg['context_precision']}")
    print("=" * 80)


if __name__ == "__main__":
    run_fallback_eval(Path("datasets/testset_full.jsonl"), Path("config/chatbot.yaml"))
