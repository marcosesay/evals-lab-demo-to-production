# Demo to Production: An Evals Lab for Enterprise AI

**Policy Copilot for Meridian Crest Bank (fictional training exercise)**

## Why evals matter

A prototype can sound convincing while citing the wrong rule, inventing an answer, or failing to recognize that a question is outside its source material. That gap matters in an operations setting: a confident but unsupported answer can create customer, compliance, and operational risk. Evals give the team a repeatable way to measure correctness, citations, and safe handling before expanding a pilot. They also make iteration faster: change a prompt or source, rerun the same cases, and see what improved or regressed.

## Setup (under 5 minutes)

Requires Python 3.11+ and an OpenAI API key with access to the selected model and file search.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your key to .env
```

The first question uploads the fictional manual to an OpenAI vector store and saves its ID in `.vector_store_id`. Later runs reuse that store. The vector store ID and API key are local configuration and are ignored by Git.

## Module 1: Build the agent

The manual in `data/policy_manual.md` is uploaded to OpenAI file search. The Agents SDK exposes that vector store through a hosted `FileSearchTool`, so the model can retrieve relevant sections while answering. The default model is `gpt-4.1-mini`; set `OPENAI_MODEL` in `.env` to try another supported model.

Ask a question:

```bash
python -m src.agent --version v2 "What is the callback threshold for domestic wires?"
```

Try `--version v1` to use the short first-demo prompt. Both versions use the same model, source, retrieval tool, and eval set; only their instruction text differs.

## Module 2: Measure it

`data/eval_set.jsonl` has 26 hand-authored cases: 14 direct lookups, 5 exception or multi-section reasoning cases, and 7 trap questions. Direct cases check retrieval and basic grounding. Reasoning cases catch answers that overlook scope or combine limits incorrectly. Trap questions test whether the assistant can recognize the source boundary. A model that answers every question fluently can still be unsafe if it invents policy outside the manual.

Run any version:

```bash
python -m src.run_evals --version v1
python -m src.run_evals --version v2
python -m src.run_evals --version v3
```

Each answer is graded by an LLM judge against the expected substance, citation, and refusal behavior. Results are written to `results/<version>_results.jsonl`. Review individual records as well as the aggregate: an LLM judge is a useful repeatable signal, not a substitute for human review of high-impact decisions.

## Module 3: Improve it

V1 is intentionally the simple first-demo instruction: “You are a helpful bank policy assistant. Answer the user's question.” V2 adds boundaries the production task needs: use retrieved manual text only, cite a section in a fixed format, decline unsupported questions and route them to a team, and keep responses concise. V3 uses the same grounding and refusal approach with a Pydantic output schema for the answer, supporting section IDs, and coverage status. The code renders the answer and source line from those structured fields. V1 is not deliberately weakened; it is a realistic starting point.

After all three runs, compare case outcomes:

```bash
python -m src.compare
```

Review cases whose outcomes differ across versions, then inspect their full answers in the result files. A better pass rate is evidence that a change helped this test set; it does not prove readiness for every real request. Inspect trap failures first, then add targeted cases for the failure pattern and consider a retrieval-quality improvement.

## Results

Measured with `gpt-4.1-mini` using the 26-case eval set, including three domestic wire callback cases and three out-of-scope traps. Overall means all three criteria passed. The V3 row reflects the revised structured-output rules for direct topic matching, deterministic escalation when uncovered, and complete multi-part answers.

| Version | Correctness | Citation | Refusal | Overall | Direct | Reasoning | Trap | Trap hallucinations |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| V1 | 88% | 50% | 92% | 38% (10/26) | 36% (5/14) | 20% (1/5) | 57% (4/7) | 2 |
| V2 | 96% | 62% | 96% | 58% (15/26) | 43% (6/14) | 60% (3/5) | 86% (6/7) | 1 |
| V3 | 100% | 100% | 100% | 100% (26/26) | 100% (14/14) | 100% (5/5) | 100% (7/7) | 0 |

## Held-out results

This separate 8-case set covers less-tested policy sections and four topics absent from the manual. The prompts were unchanged for these runs. To reproduce them, use `--dataset holdout`:

```bash
python -m src.run_evals --version v1 --dataset holdout
python -m src.run_evals --version v2 --dataset holdout
python -m src.run_evals --version v3 --dataset holdout
```

| Version | Correctness | Citation | Refusal | Overall | Direct (3) | Reasoning (1) | Traps (4) | Trap hallucinations |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| V1 | 100% | 100% | 100% | 100% (8/8) | 100% | 100% | 100% | 0 |
| V2 | 100% | 50% | 100% | 50% (4/8) | 0% | 0% | 100% | 0 |
| V3 | 100% | 100% | 100% | 100% (8/8) | 100% | 100% | 100% | 0 |

## What to tell your exec sponsor

“We now have a repeatable measurement gate for the Policy Copilot: it checks whether answers match policy, cite the supporting section, and decline requests outside the manual. The measured results show where the assistant is reliable and where controls or source coverage still need work, giving us a concrete basis for a limited, monitored rollout decision rather than relying on a persuasive demo.”

## Exercises

1. Add three test cases for one policy area, including one boundary value, then rerun both versions.
2. Change `OPENAI_MODEL`, rerun the evals, and compare quality, latency, and cost for your environment.
3. Add a clearly labeled policy section and two supporting eval cases; check that retrieval finds the new section and the answer cites it.

## Workshop boundaries

The manual is fictional and for training only. Do not use it to make real customer or banking decisions. The API calls send the synthetic manual and questions to OpenAI. Never put real customer information in this demo.
