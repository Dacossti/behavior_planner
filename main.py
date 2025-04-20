# main.py
# Title: End‑to‑End AI2-THOR Planner-Executor
# ------------------------------------------------
# Parses instructions, generates PDDL, plans, executes using AI2-THOR

from llm_parser import parse_instruction_to_subgoals
from pddl_utils import subgoals_to_pddl
from pddl_planner import run_planner
from pathlib import Path
import gym
import kitchen_gym.kitchen_nav_env

PDDL_TO_ENV_ACTION = {
    "move": 0,
    "rotateleft": 1,
    "rotateright": 2,
    "pickup": 3,
    "place": 4,
}

def execute_plan(plan: list):
    env = gym.make('KitchenNav-v0')
    obs = env.reset()

    for pddl_action in plan:
        print("Executing:", pddl_action)
        parts = pddl_action.lower().split()
        action_name = parts[0]

        if action_name in PDDL_TO_ENV_ACTION:
            action_idx = PDDL_TO_ENV_ACTION[action_name]
            obs, reward, done, info = env.step(action_idx)
            print(f"Action {action_name} executed. Reward: {reward}, Done: {done}")
        else:
            print(f"Unknown PDDL action: {pddl_action}")

    env.close()

if __name__ == "__main__":
    instr = input("Enter instruction: ")
    subgoals = parse_instruction_to_subgoals(instr)
    print("Subgoals:", subgoals)

    domain_str, problem_str = subgoals_to_pddl(subgoals)

    plan = run_planner(domain_str, problem_str)
    print("Plan:", plan)

    execute_plan(plan)