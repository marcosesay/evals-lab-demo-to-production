"""Compare completed v1, v2, and v3 eval runs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = ("v1", "v2", "v3")
CRITERIA = ("correctness", "citation", "refusal")


def read(version: str) -> dict[str, dict]:
    path = ROOT / "results" / f"{version}_results.jsonl"
    return {
        row["id"]: row
        for row in (
            json.loads(line)
            for line in path.read_text().splitlines()
            if line.strip()
        )
    }


def main() -> None:
    results = {version: read(version) for version in VERSIONS}
    ids = sorted(set().union(*(set(rows) for rows in results.values())))

    print(f"{'Case':<6} {'Category':<12} {'V1':<7} {'V2':<7} {'V3':<7}")
    for case_id in ids:
        rows = [results[version].get(case_id) for version in VERSIONS]
        category = next((row["category"] for row in rows if row), "—")
        states = [("PASS" if row and row["pass"] else "FAIL") for row in rows]
        print(f"{case_id:<6} {category:<12} {states[0]:<7} {states[1]:<7} {states[2]:<7}")

    print("\nOverall pass counts")
    for version in VERSIONS:
        rows = list(results[version].values())
        passed = sum(row["pass"] for row in rows)
        print(f"{version.upper()}: {passed}/{len(rows)} ({passed / len(rows):.0%})")

    print("\nCases with criterion changes")
    changed = False
    for case_id in ids:
        rows = [results[version].get(case_id) for version in VERSIONS]
        if not all(rows):
            continue
        differences = [
            f"{criterion}: " + "/".join(
                ("PASS" if row["pass"] else "FAIL") if criterion == "pass" else row[criterion].upper()
                for row in rows
            )
            for criterion in (*CRITERIA, "pass")
            if len({row[criterion] for row in rows}) > 1
        ]
        if differences:
            changed = True
            print(f"{case_id}: {'; '.join(differences)}")
    if not changed:
        print("None")


if __name__ == "__main__":
    main()
