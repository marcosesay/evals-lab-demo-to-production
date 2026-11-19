"""Run the JSONL eval set and grade answers with an LLM judge."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import time
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
from openai import AuthenticationError, OpenAI

from .agent import MODEL, ROOT, answer
from .prompts import JUDGE_PROMPT

CRITERIA = ("correctness", "citation", "refusal")
MAX_429_RETRIES = 5
MAX_AUTOMATIC_WAIT_SECONDS = 120
SECTION_ID_PATTERN = re.compile(r"\bOPS-\d+\.\d+\b")
MANUAL_TEXT = (ROOT / "data" / "policy_manual.md").read_text()
KNOWN_SECTION_IDS = set(SECTION_ID_PATTERN.findall(MANUAL_TEXT))


class RateLimitDeferred(RuntimeError):
    """A rate limit requires a longer wait than this CLI should block for."""


def is_rate_limit(error: Exception) -> bool:
    return getattr(error, "status_code", None) == 429


def retry_delay(attempt: int) -> float:
    return min(2 ** attempt, 30)


def recommended_retry_delay(error: Exception) -> float | None:
    """Read a server retry hint where available, including durations in 429 text."""
    response = getattr(error, "response", None)
    headers = getattr(response, "headers", {}) or {}
    header_delay = headers.get("retry-after")
    if header_delay:
        try:
            return max(0.0, float(header_delay))
        except ValueError:
            pass

    message = str(error)
    duration = re.search(r"(?:try again in|reset(?:s)? in)\s*(?:(\d+)m)?\s*(\d+(?:\.\d+)?)s", message, re.I)
    if duration:
        return int(duration.group(1) or 0) * 60 + float(duration.group(2))
    return None


def handle_rate_limit(error: Exception, attempt: int, operation: str) -> float:
    server_delay = recommended_retry_delay(error)
    delay = server_delay if server_delay is not None else retry_delay(attempt)
    if delay > MAX_AUTOMATIC_WAIT_SECONDS:
        minutes, seconds = divmod(round(delay), 60)
        wait_text = f"{minutes}m {seconds}s" if minutes else f"{seconds}s"
        raise RateLimitDeferred(
            f"The {operation} request is rate limited; the API asked for a {wait_text} wait. "
            "Stopping here so the command does not block for a long time. "
            "Rerun with --resume after the limit resets; completed cases are saved."
        ) from error
    return delay


def judge(client: OpenAI, case: dict, response: str) -> dict:
    payload = {
        "question": case["question"], "expected_answer": case["expected_answer"],
        "expected_section": case["expected_section"], "category": case["category"],
        "assistant_answer": response,
    }
    for attempt in range(MAX_429_RETRIES + 1):
        try:
            result = client.responses.create(
                model=MODEL,
                input=[{"role": "system", "content": JUDGE_PROMPT},
                       {"role": "user", "content": json.dumps(payload)}],
            )
            break
        except Exception as error:
            if not is_rate_limit(error) or attempt == MAX_429_RETRIES:
                raise
            delay = handle_rate_limit(error, attempt, "judge")
            print(f"  Judge rate limited (429); retrying in {delay}s.")
            time.sleep(delay)
    raw = result.output_text.strip()
    try:
        scores = json.loads(raw)
    except json.JSONDecodeError:
        start, end = raw.find("{"), raw.rfind("}")
        scores = json.loads(raw[start:end + 1])
    for key in ("correctness", "refusal"):
        scores[key] = "pass" if str(scores.get(key, "fail")).lower() == "pass" else "fail"
    return scores


def grade_citation(case: dict, response: str) -> str:
    if case["category"] == "trap":
        cited_ids = SECTION_ID_PATTERN.findall(response)
        return "pass" if all(section_id in KNOWN_SECTION_IDS for section_id in cited_ids) else "fail"
    expected_section = case.get("expected_section")
    return "pass" if expected_section and expected_section in response else "fail"


async def answer_with_retry(question: str, version: str) -> str:
    for attempt in range(MAX_429_RETRIES + 1):
        try:
            return await answer(question, version)
        except Exception as error:
            if not is_rate_limit(error) or attempt == MAX_429_RETRIES:
                raise
            delay = handle_rate_limit(error, attempt, "agent")
            print(f"  Agent rate limited (429); retrying in {delay}s.")
            await asyncio.sleep(delay)
    raise RuntimeError("Unreachable retry state")


def print_case_result(index: int, total: int, row: dict) -> None:
    criteria = " ".join(f"{name}={row[name].upper()}" for name in CRITERIA)
    status = "PASS" if row["pass"] else "FAIL"
    print(f"[{index:02}/{total}] {row['id']} {criteria} overall={status}")
    if not row["pass"]:
        failed = [name for name in CRITERIA if row[name] == "fail"]
        reason = " ".join(str(row.get("reason", "")).split())
        print(f"  Failed: {', '.join(failed)}. {reason}")


async def run(version: str, resume: bool = False, dataset: str = "eval") -> list[dict]:
    load_dotenv(ROOT / ".env")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required. Copy .env.example to .env and add your key.")
    client = OpenAI()
    dataset_path = ROOT / "data" / ("eval_set.jsonl" if dataset == "eval" else "holdout_set.jsonl")
    cases = [json.loads(line) for line in dataset_path.read_text().splitlines() if line.strip()]
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    result_suffix = "_holdout" if dataset == "holdout" else ""
    result_path = out_dir / f"{version}{result_suffix}_results.jsonl"
    results = []
    if resume and result_path.exists():
        results = [json.loads(line) for line in result_path.read_text().splitlines() if line.strip()]
    completed_ids = {row["id"] for row in results}
    mode = "a" if resume else "w"
    with result_path.open(mode) as result_file:
        for case in cases:
            if case["id"] in completed_ids:
                continue
            response = await answer_with_retry(case["question"], version)
            scores = judge(client, case, response)
            scores["citation"] = grade_citation(case, response)
            passed = all(scores[key] == "pass" for key in CRITERIA)
            row = {**case, "response": response, **scores, "pass": passed}
            result_file.write(json.dumps(row, ensure_ascii=False) + "\n")
            result_file.flush()
            results.append(row)
            completed_ids.add(case["id"])
            print_case_result(len(completed_ids), len(cases), row)
    return results


def print_summary(version: str, rows: list[dict]) -> None:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["category"]].append(row)
    print(f"\n{version.upper()} results")
    print("Category     N   Correctness  Citation  Refusal  Overall")
    for category in ("direct", "reasoning", "trap", "all"):
        group = rows if category == "all" else groups[category]
        rates = [sum(row[key] == "pass" for row in group) / len(group) if group else 0 for key in CRITERIA]
        passed = sum(row["pass"] for row in group)
        overall = passed / len(group) if group else 0
        print(f"{category:<12} {len(group):>2}  {rates[0]:>10.0%}  {rates[1]:>7.0%}  {rates[2]:>6.0%}  {overall:>7.0%}")
    hallucinations = sum(row["category"] == "trap" and row["refusal"] == "fail" for row in rows)
    print("Overall is the share passing all three criteria; case lines identify the failed criterion(s).")
    print(f"Trap hallucination count (failed to decline and escalate): {hallucinations}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", choices=("v1", "v2", "v3"), required=True)
    parser.add_argument("--dataset", choices=("eval", "holdout"), default="eval")
    parser.add_argument("--resume", action="store_true", help="Skip cases already recorded in the result file")
    args = parser.parse_args()
    try:
        rows = asyncio.run(run(args.version, resume=args.resume, dataset=args.dataset))
    except RateLimitDeferred as error:
        print(f"Rate limit: {error}")
        raise SystemExit(2) from None
    except AuthenticationError:
        print("Authentication failed. Check that OPENAI_API_KEY in .env is a valid API key (with only one 'sk-' prefix).")
        raise SystemExit(2) from None
    print_summary(args.version, rows)


if __name__ == "__main__":
    main()
