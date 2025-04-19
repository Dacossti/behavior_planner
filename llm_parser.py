# instruction_parser.py
# Title: Natural Language → Subgoal Sequence
# ------------------------------------------------
# Uses a pretrained LLM (e.g. via OpenAI API) to turn
# a free‑form instruction into an ordered list of
# symbolic subgoals.

import os
import openai  # pip install openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_instruction_to_subgoals(instruction: str) -> list:
    """
    Query the LLM to break an instruction into subgoals.
    Returns a list like ['GoToKitchen', 'PickUpPlate', ...].
    """
    prompt = f"You are an assistant that converts household instructions into a step-by-step sequence of subgoals. Instruction: '{instruction}' Output as a JSON list of steps, e.g. ['GoToKitchen', 'PickUpPlate', 'PlacePlateOnTable']"
    
    resp = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[{"role": "system", "content": "You output only a JSON list."},
                  {"role": "user", "content": prompt}]
    )
    # parse JSON from the assistant’s reply
    subgoals = resp.choices[0].message.content.strip()
    return json.loads(subgoals)

if __name__ == "__main__":
    instr = "Set the table for two."
    print(parse_instruction_to_subgoals(instr))
