# kitchen_nav_env.py
# Title: AI2-THOR Kitchen Navigation Environment Variants
# ------------------------------------------------------
# Custom Gym wrapper around AI2-THOR with different skill modes.

import gym
from gym import spaces
import numpy as np
import ai2thor.controller

class KitchenNavEnv(gym.Env):
    """
    AI2-THOR Gym Environment for household embodied agents.
    Supports navigation, object pickup, and object placement.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, mode="nav"):
        super(KitchenNavEnv, self).__init__()
        self.controller = ai2thor.controller.Controller()
        self.controller.start()

        # Load kitchen scene
        self.controller.reset('FloorPlan1')

        # Define action space depending on mode
        self.mode = mode.lower()
        if self.mode == "nav":
            self.action_space = spaces.Discrete(5)  # MoveAhead, RotateLeft, RotateRight, PickupObject, PlaceObject
        elif self.mode == "pickup":
            self.action_space = spaces.Discrete(2)  # PickupObject, RotateLeft
        elif self.mode == "place":
            self.action_space = spaces.Discrete(2)  # PlaceObject, RotateLeft
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

        # Observation space (RGB image)
        self.observation_space = spaces.Box(low=0, high=255, shape=(300, 300, 3), dtype=np.uint8)

    def step(self, action):
        if self.mode == "nav":
            if action == 0:
                self.controller.step(action='MoveAhead')
            elif action == 1:
                self.controller.step(action='RotateLeft')
            elif action == 2:
                self.controller.step(action='RotateRight')
            elif action == 3:
                self.controller.step(action='PickupObject', objectId="Plate|+00.50|+00.00|+01.00")
            elif action == 4:
                self.controller.step(action='PutObject', objectId="Plate|+00.50|+00.00|+01.00")
        elif self.mode == "pickup":
            if action == 0:
                self.controller.step(action='PickupObject', objectId="Plate|+00.50|+00.00|+01.00")
            elif action == 1:
                self.controller.step(action='RotateLeft')
        elif self.mode == "place":
            if action == 0:
                self.controller.step(action='PutObject', objectId="Plate|+00.50|+00.00|+01.00")
            elif action == 1:
                self.controller.step(action='RotateLeft')

        obs = self.get_observation()

        # Dummy reward logic for now — improve as needed
        reward = 0
        done = False
        info = {}

        return obs, reward, done, info

    def reset(self):
        self.controller.reset('FloorPlan1')
        return self.get_observation()

    def get_observation(self):
        event = self.controller.last_event
        return event.frame

    def render(self, mode='human'):
        pass  # Optional rendering

    def close(self):
        self.controller.stop()

# --------- ENV REGISTRATION ---------
from gym.envs.registration import register

register(
    id='KitchenNav-v0',
    entry_point='kitchen_gym.kitchen_nav_env:KitchenNavEnv',
    kwargs={'mode': 'nav'}
)

register(
    id='PickupOnly-v0',
    entry_point='kitchen_gym.kitchen_nav_env:KitchenNavEnv',
    kwargs={'mode': 'pickup'}
)

register(
    id='PlaceOnly-v0',
    entry_point='kitchen_gym.kitchen_nav_env:KitchenNavEnv',
    kwargs={'mode': 'place'}
)