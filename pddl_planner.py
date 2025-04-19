# pddl_planner.py
# Title: File‑Based PDDL Planner
# ------------------------------------------------
# Reads a PDDL domain and problem from disk, invokes
# Fast Downward, and returns a list of grounded actions.

import subprocess
import tempfile
from pathlib import Path

def load_pddl_file(path: Path) -> str:
    """
    Read the entire contents of a PDDL file.
    Raises FileNotFoundError if the file doesn’t exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"PDDL file not found: {path}")
    return path.read_text()

def run_planner(domain_str: str, problem_str: str) -> list:
    """
    Write domain & problem strings into temporary .pddl files,
    call Fast Downward, and parse its output plan into a Python list.
    """
    # 1) Create two temp files for domain and problem
    with tempfile.NamedTemporaryFile("w", suffix=".pddl", delete=False) as d, \
         tempfile.NamedTemporaryFile("w", suffix=".pddl", delete=False) as p:
        d.write(domain_str)
        p.write(problem_str)
        domain_file = d.name
        problem_file = p.name

    # 2) Invoke the planner (assumes fast‑downward.py is on your PATH)
    result = subprocess.run(
        ["fast-downward.py", "--plan-file", "plan.txt", domain_file, problem_file],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Planner error:\n{result.stderr}")

    # 3) Read back the plan
    with open("plan.txt") as f:
        actions = [line.strip() for line in f if line.strip()]
    return actions

if __name__ == "__main__":
    # 1. Locate PDDL files (expects a 'domain/' folder next to this script)
    base = Path(__file__).parent / "domain"
    domain_path  = base / "domain.pddl"
    problem_path = base / "problem.pddl"

    # 2. Load their contents
    domain_str  = load_pddl_file(domain_path)
    problem_str = load_pddl_file(problem_path)

    # 3. Run the planner and print the resulting action sequence
    plan = run_planner(domain_str, problem_str)
    print("Plan:", plan)