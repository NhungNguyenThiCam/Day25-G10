from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from dotenv import load_dotenv
from langsmith import Client

from vna_chatbot import answer_question, load_config, load_pages, retrieve_pages


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def sync_dataset(dataset_name: str, input_path: Path, config_path: Path) -> None:
    load_dotenv()
    config = load_config(config_path)
    client = Client()
    if client.has_dataset(dataset_name):
        dataset = client.read_dataset(dataset_name=dataset_name)
    else:
        dataset = client.create_dataset(dataset_name=dataset_name, description="Vietnam Airlines chatbot testset")

    examples = read_jsonl(input_path)
    existing_questions = {
        example.inputs.get(config.langsmith.get("input_key", "question"), "")
        for example in client.list_examples(dataset_id=dataset.id)
    }

    created = 0
    for example in examples:
        question_key = config.langsmith.get("input_key", "question")
        question = example[question_key]
        if question in existing_questions:
            continue

        inputs = {question_key: question}
        outputs = {}
        if config.langsmith.get("reference_key") in example:
            outputs[config.langsmith.get("reference_key")] = example[config.langsmith.get("reference_key")]
        client.create_example(dataset_id=dataset.id, inputs=inputs, outputs=outputs)
        created += 1

    print(f"Synced {created} new examples to LangSmith dataset: {dataset_name}")


def run_local_benchmark(dataset_path: Path, config_path: Path) -> None:
    load_dotenv()
    config = load_config(config_path)
    pages = load_pages(config.data_path)
    examples = read_jsonl(dataset_path)

    for example in examples:
        question = example.get(config.langsmith.get("input_key", "question"), "")
        result = answer_question(question, config, pages)
        print(json.dumps({"question": question, "answer": result["answer"], "sources": result["sources"]}, ensure_ascii=False, indent=2))


def run_ragas_eval(dataset_path: Path, config_path: Path) -> None:
    load_dotenv()
    config = load_config(config_path)
    pages = load_pages(config.data_path)
    examples = read_jsonl(dataset_path)

    prepared_rows: list[dict] = []
    for example in examples:
        question = example.get(config.langsmith.get("input_key", "question"), "")
        reference = example.get(config.langsmith.get("reference_key", "reference"), "")
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

    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import answer_relevancy, context_precision, faithfulness
    except ImportError as exc:
        raise SystemExit(
            "ragas/datasets chưa được cài. Hãy chạy pip install -r requirements.txt rồi thử lại."
        ) from exc

    dataset = Dataset.from_list(prepared_rows)
    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision],
    )
    print(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="LangSmith dataset utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync-dataset", help="Create a LangSmith dataset from JSONL")
    sync_parser.add_argument("--dataset-name", required=True)
    sync_parser.add_argument("--input-file", required=True)
    sync_parser.add_argument("--config", default="config/chatbot.yaml")

    run_parser = subparsers.add_parser("run-local", help="Run the chatbot locally on a JSONL testset")
    run_parser.add_argument("--input-file", required=True)
    run_parser.add_argument("--config", default="config/chatbot.yaml")

    ragas_parser = subparsers.add_parser("run-ragas", help="Run RAGAS eval on a JSONL testset")
    ragas_parser.add_argument("--input-file", required=True)
    ragas_parser.add_argument("--config", default="config/chatbot.yaml")

    args = parser.parse_args()

    if args.command == "sync-dataset":
        sync_dataset(args.dataset_name, Path(args.input_file), Path(args.config))
    elif args.command == "run-local":
        run_local_benchmark(Path(args.input_file), Path(args.config))
    elif args.command == "run-ragas":
        run_ragas_eval(Path(args.input_file), Path(args.config))


if __name__ == "__main__":
    main()
