# main.py
# Title: End‑to‑End Planner + Executor
# ------------------------------------------------
# Integrates instruction parsing, PDDL planning, and
# skill execution/monitoring in a loop.

from llm_parser import parse_instruction_to_subgoals
from pddl_planner import subgoals_to_pddl, run_planner
from stable_baselines3 import PPO

# Mapping from PDDL action → skill model
ACTION_TO_SKILL = {
    "move": "nav_skill.zip",
    "pick": "pick_skill.zip",
    "place": "place_skill.zip",
}

def execute_plan(actions: list):
    """
    For each action in the classical plan,
    load the corresponding skill and execute it until success.
    """
    for act in actions:
        # e.g., act = 'move Kitchen'
        name, arg = act.split()
        skill = PPO.load(ACTION_TO_SKILL[name])
        done = False
        obs = None
        while not done:
            action, _ = skill.predict(obs)  # feed current obs
            obs, reward, done, info = skill.env.step(action)
        print(f"{act} succeeded.")

if __name__ == "__main__":
    instr = input("Enter instruction: ")
    subgoals = parse_instruction_to_subgoals(instr)
    domain, problem = subgoals_to_pddl(subgoals)
    plan = run_planner(domain, problem)
    print("Plan:", plan)
    execute_plan(plan)
