"""Policy Copilot backed by an OpenAI hosted file-search vector store."""
from __future__ import annotations

import argparse
import asyncio
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from agents import Agent, FileSearchTool, Runner
from openai import NotFoundError, OpenAI
from pydantic import BaseModel, Field

from .prompts import V1_INSTRUCTIONS, V2_INSTRUCTIONS, V3_INSTRUCTIONS

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
MANUAL = ROOT / "data" / "policy_manual.md"
STORE_ID_FILE = ROOT / ".vector_store_id"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


class PolicyCopilotOutput(BaseModel):
    answer: str = Field(description="A concise answer grounded only in the retrieved policy manual")
    section_ids: list[str] = Field(description="Exact OPS-x.y IDs that support the answer; empty when not covered")
    covered: bool = Field(description="Whether the manual supports answering the question")
    escalate_to: str = Field(description="Escalation team or role only; use an appropriate qualified team or manager if the manual names none")


def get_vector_store_id() -> str:
    load_dotenv(ROOT / ".env")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required. Copy .env.example to .env and add your key.")
    client = OpenAI()
    if STORE_ID_FILE.exists():
        store_id = STORE_ID_FILE.read_text().strip()
        try:
            client.vector_stores.retrieve(store_id)
            return store_id
        except NotFoundError:
            STORE_ID_FILE.unlink(missing_ok=True)
    store = client.vector_stores.create(name="Meridian Crest fictional policy manual")
    with MANUAL.open("rb") as manual_file:
        client.vector_stores.file_batches.upload_and_poll(vector_store_id=store.id, files=[manual_file])
    STORE_ID_FILE.write_text(store.id + "\n")
    return store.id


def make_agent(version: str) -> Agent:
    instructions = {"v1": V1_INSTRUCTIONS, "v2": V2_INSTRUCTIONS, "v3": V3_INSTRUCTIONS}[version]
    return Agent(
        name="Meridian Crest Policy Copilot",
        instructions=instructions,
        model=MODEL,
        tools=[FileSearchTool(vector_store_ids=[get_vector_store_id()], max_num_results=5)],
        **({"output_type": PolicyCopilotOutput} if version == "v3" else {}),
    )


async def answer(question: str, version: str = "v2") -> str:
    result = await Runner.run(make_agent(version), question)
    if version == "v3":
        output = result.final_output
        if not isinstance(output, PolicyCopilotOutput):
            output = PolicyCopilotOutput.model_validate(output)
        if not output.covered:
            escalate_to = output.escalate_to.strip() or "the appropriate qualified team or manager"
            rendered = (
                "This isn't covered in the Meridian Crest operations manual. "
                f"Please escalate to {escalate_to}."
            )
        else:
            rendered = output.answer.strip()
            if output.section_ids:
                rendered += "\nSource: " + ", ".join(output.section_ids)
        return clean_response_text(rendered)
    return clean_response_text(str(result.final_output))


def clean_response_text(text: str) -> str:
    """Remove punctuation fragments left after file-search annotations are stripped."""
    text = re.sub(r",\s*\.", ".", text)
    text = re.sub(r"\s+and\s+\.", ".", text, flags=re.IGNORECASE)
    return re.sub(r"\s+([,.!?])", r"\1", text).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the fictional Policy Copilot")
    parser.add_argument("--version", choices=("v1", "v2", "v3"), default="v2")
    parser.add_argument("question", nargs="+", help="Question to ask")
    args = parser.parse_args()
    print(asyncio.run(answer(" ".join(args.question), args.version)))


if __name__ == "__main__":
    main()
