# pddl_utils.py
# Title: Subgoals → PDDL Strings
# ------------------------------------------------
# Converts subgoals into PDDL domain & problem definitions

PDDL_DOMAIN = """
(define (domain house)
  (:predicates (at ?x) (holding ?o) (placed ?o ?r))
  (:action move
    :parameters (?from ?to)
    :precondition (at ?from)
    :effect (and (not (at ?from)) (at ?to)))
  (:action pickup
    :parameters (?o ?r)
    :precondition (and (at ?r))
    :effect (holding ?o))
  (:action place
    :parameters (?o ?r)
    :precondition (and (holding ?o) (at ?r))
    :effect (placed ?o ?r))
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
    init = "(at LivingRoom)"
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