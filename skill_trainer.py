# skill_trainer.py
# Title: Skill‑Level RL Training
# ------------------------------------------------
# Trains individual policies (skills) for navigation, pickup,
# and placement using Stable Baselines3 + a Gym interface.

import gym
import kitchen_gym.kitchen_nav_env  # registers KitchenNav-v0, PickupOnly-v0, PlaceOnly-v0
from stable_baselines3 import PPO

def train_skill(env_name: str, model_path: str, timesteps: int = 100_000):
    env = gym.make(env_name)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=timesteps)
    model.save(model_path)
    print(f"Saved skill policy to {model_path}")

if __name__ == "__main__":
    train_skill("KitchenNav-v0", "models/nav_skill.zip")
    #train_skill("PickupOnly-v0", "pick_skill.zip")
    #train_skill("PlaceOnly-v0", "place_skill.zip")