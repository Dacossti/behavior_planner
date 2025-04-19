# pddl_planner.py
# Title: Subgoals → PDDL → Motion Plan
# ------------------------------------------------
# Converts subgoals into a PDDL problem and domain, then calls
# a classical planner (e.g., Fast Downward) or a sampling-based
# motion planner (e.g., OMPL) to get a sequence of waypoints.

import subprocess
import tempfile

PDDL_DOMAIN = """
(define (domain house)
  (:predicates (at ?x) (holding ?o) (placed ?o ?r))
  ;; ... define actions like move, pick, place
)
"""

PDDL_TEMPLATE = """
(define (problem household-job)
  (:domain house)
  (:init {init})
  (:goal (and {goal}))
)
"""

def subgoals_to_pddl(subgoals: list):
    # Build init and goal from subgoals
    init = "(at LivingRoom)"  # assume start
    goal_atoms = []
    for step in subgoals:
        if step.startswith("GoTo"):
            room = step[4:]
            goal_atoms.append(f"(at {room})")
        elif step.startswith("PickUp"):
            obj = step[6:]
            goal_atoms.append(f"(holding {obj})")
        elif step.startswith("Place"):
            obj, loc = step[5:].split("On")
            goal_atoms.append(f"(placed {obj} {loc})")
    problem = PDDL_TEMPLATE.format(init=init, goal=" ".join(goal_atoms))
    return PDDL_DOMAIN, problem

def run_planner(domain_str: str, problem_str: str) -> list:
    # Write temporary files
    with tempfile.NamedTemporaryFile("w", delete=False) as d, \
         tempfile.NamedTemporaryFile("w", delete=False) as p:
        d.write(domain_str); p.write(problem_str)
        d_path, p_path = d.name, p.name

    # Call Fast Downward (assumes it's on your PATH)
    result = subprocess.run(
        ["fast-downward.py", "--plan-file", "plan.txt", d_path, p_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    # Read back the plan as a list of actions
    with open("plan.txt") as f:
        actions = [line.strip() for line in f if line.strip()]
    return actions

if name == "__main__":
    dom, prob = subgoals_to_pddl(["GoToKitchen", "PickUpPlate", "PlacePlateOnTable"])
    plan = run_planner(dom, prob)
    print("Plan:", plan)