# llm_parser.py
# Title: LLM-Based Instruction Parser
# ------------------------------------------------
# Uses OpenAI's GPT-4 API to parse natural language instructions into subgoals.

import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_instruction_to_subgoals(instruction: str) -> list:
    """
    Sends a prompt to GPT-3.5 to convert a natural language instruction
    into a list of subgoals.
    """
    prompt = f"""
    You are an assistant helping a robot in a kitchen environment. 
    Convert the following instruction into a list of subgoals.
    Example:
    Instruction: "Pick up the cup and place it on the table"
    Subgoals:
    - GoToCupboard
    - PickUpCup
    - GoToTable
    - PlaceCupOnTable

    Now do the same for:
    Instruction: "{instruction}"
    Subgoals:
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    subgoals_text = response.choices[0].message.content
    subgoals = [line.strip("- ").strip() for line in subgoals_text.strip().split("\n") if line.strip()]

    return subgoals

if __name__ == "__main__":
    instr = input("Enter instruction: ")
    subgoals = parse_instruction_to_subgoals(instr)
    print("Subgoals:", subgoals)