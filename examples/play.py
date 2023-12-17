import sys
import os

# Load `simon_arc_env` from the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import simon_arc_env

import gymnasium as gym
import pygame

env = gym.make(
    "SimonARC-v0", 
    render_mode="human",
    #path_to_task_dir="/Users/youname/arc-dataset/evaluation"
)
keys_to_action = env.unwrapped.keys_to_action()

env.reset()
playing = True
while playing:
    env.render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
            if event.key == pygame.K_i:
                obs = env.unwrapped.observation
                print("Inspect", obs)
            if event.key in keys_to_action: 
                action = keys_to_action[event.key]
                observation, reward, terminated, truncated, info = env.step(action)
                if reward > 0:
                    print("Reward", reward)
                if terminated:
                    print("Terminated")
                    playing = False
                if truncated:
                    print("Truncated")
                    playing = False

env.close()
