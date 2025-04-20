# pddl_utils.py
# Title: Subgoals → PDDL Problem String
# ------------------------------------------------
# Loads domain.pddl from disk and builds problem.pddl based on subgoals.

from pathlib import Path

# Paths
BASE = Path(__file__).parent / "domain"
DOMAIN_PATH = BASE / "domain.pddl"
PROBLEM_TEMPLATE_PATH = BASE / "problem_template.pddl"

def load_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"PDDL file not found: {path}")
    return path.read_text()

# Load domain.pddl content
PDDL_DOMAIN = load_file(DOMAIN_PATH)

# Load problem template content
PDDL_TEMPLATE = load_file(PROBLEM_TEMPLATE_PATH)

def subgoals_to_pddl(subgoals: list):
    """
    Converts subgoals into a PDDL problem string using problem_template.pddl.
    """
    # Hardcoded initial state for now (matching your problem.pddl)
    init = """(at agent1 LivingRoom)
    (at-object Plate1 Table)
    (at-object Cup1 Table)
    (empty-hand agent1)"""

    # Build goal predicates based on subgoals
    goal_atoms = []
    for step in subgoals:
        if step.startswith("GoTo"):
            room = step[4:]
            goal_atoms.append(f"(at agent1 {room})")
        elif step.startswith("PickUp"):
            obj = step[6:]
            goal_atoms.append(f"(holding agent1 {obj})")
        elif step.startswith("Place"):
            obj, loc = step[5:].split("On")
            goal_atoms.append(f"(placed {obj} {loc})")
    
    # Format the problem string with init and goal
    problem_str = PDDL_TEMPLATE.format(
        init=init,
        goal="\n    ".join(goal_atoms)
    )

    return PDDL_DOMAIN, problem_str