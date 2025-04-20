# pddl_planner.py
# Title: PDDL Planner Runner
# ------------------------------------------------
# Runs Fast Downward on PDDL strings and returns action sequence

import subprocess
import tempfile

def run_planner(domain_str: str, problem_str: str) -> list:
    with tempfile.NamedTemporaryFile("w", suffix=".pddl", delete=False) as d, \
         tempfile.NamedTemporaryFile("w", suffix=".pddl", delete=False) as p:
        d.write(domain_str)
        p.write(problem_str)
        domain_file, problem_file = d.name, p.name

    result = subprocess.run(
        ["./downward/fast-downward.py", "--plan-file", "plan.txt", domain_file, problem_file],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Planner error:\n{result.stderr}")

    with open("plan.txt") as f:
        actions = [line.strip() for line in f if line.strip()]
    return actions