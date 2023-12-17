import sys
import os
import gymnasium as gym
import time

# Load `simon_arc_env` from the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import simon_arc_env

env = gym.make("SimonARC-v0", render_mode="human")

for episode in range(5):
    (observation,_) = env.reset()
    terminated = False
    truncated = False
    score = 0
    while not terminated and not truncated:
        time.sleep(0.01)
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        score += reward

    print("Episode: {} Score: {}".format(episode, score))

env.close()
