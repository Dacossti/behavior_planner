# skill_trainer.py
# Title: Skill‑Level RL Training
# ------------------------------------------------
# Trains individual policies (skills) for navigation, pickup,
# and placement using Stable Baselines3 + a Gym interface.

import gym
from stable_baselines3 import PPO

def train_skill(env_name: str, model_path: str, timesteps: int = 100_000):
    """
    Given a Gym environment (e.g. 'KitchenNav-v0'),
    train a PPO policy and save it.
    """
    env = gym.make(env_name)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=timesteps)
    model.save(model_path)
    print(f"Saved skill policy to {model_path}")

if name == "__main__":
    # Example: train navigation skill
    train_skill("KitchenNav-v0", "nav_skill.zip")
    # Then: train pick / place similarly