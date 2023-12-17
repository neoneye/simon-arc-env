# Best algorithm so far
# 1. DQN
# 2. A2C
# 3. PPO
#
# Training stats.
# PROMPT> tensorboard --logdir logs
# Serving TensorBoard on localhost; to expose to the network, use a proxy or pass --bind_all
# TensorBoard 2.13.0 at http://localhost:6006/ (Press CTRL+C to quit)
#
# Johnny Code: How to Solve Gymnasium MoJoCo Humanoid-v4 with Python & Stable Baseline3 | RL Tutorial 4 
# https://www.youtube.com/watch?v=OqvXHi_QtT0
# https://github.com/johnnycode8/gym_solutions/blob/main/sb3.py
#
# sentdex: Saving and Loading Models - Stable Baselines 3 Tutorial (P.2)
# https://www.youtube.com/watch?v=dLP-2Y6yu70

# sentdex: Custom Environments - Reinforcement Learning with Stable Baselines 3 (P.3)
# https://www.youtube.com/watch?v=uKnjGn8fF70
import gymnasium as gym
from stable_baselines3 import SAC, TD3, A2C, PPO, DDPG, DQN, HER
import sys
import os
import argparse

# Load `simon_arc_env` from the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import simon_arc_env

# Create directories to hold models and logs
model_dir = "models"
log_dir = "logs"
os.makedirs(model_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

def train(env, sb3_algo):
    # Available algorithms
    # https://stable-baselines3.readthedocs.io/en/master/guide/algos.html
    match sb3_algo:
        case 'A2C':
            model = A2C('MlpPolicy', env, verbose=1, tensorboard_log=log_dir)
        case 'DDPG':
            model = DDPG('MlpPolicy', env, verbose=1, tensorboard_log=log_dir)
        case 'DQN':
            model = DQN('MlpPolicy', env, verbose=1, tensorboard_log=log_dir)
        case 'HER':
            model = HER('MlpPolicy', env, verbose=1, tensorboard_log=log_dir)
        case 'PPO':
            model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=log_dir)
        case 'SAC':
            model = SAC('MlpPolicy', env, verbose=1, tensorboard_log=log_dir)
        case 'TD3':
            model = TD3('MlpPolicy', env, verbose=1, tensorboard_log=log_dir)
        case _:
            print('Algorithm not found')
            return

    TIMESTEPS = 25000
    iters = 0
    while True:
        iters += 1

        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)
        model.save(f"{model_dir}/{sb3_algo}_{TIMESTEPS*iters}")

def test(env, sb3_algo, path_to_model):

    match sb3_algo:
        case 'A2C':
            model = A2C.load(path_to_model, env=env)
        case 'DDPG':
            model = DDPG.load(path_to_model, env=env)
        case 'DQN':
            model = DQN.load(path_to_model, env=env)
        case 'HER':
            model = HER.load(path_to_model, env=env)
        case 'PPO':
            model = PPO.load(path_to_model, env=env)
        case 'SAC':
            model = SAC.load(path_to_model, env=env)
        case 'TD3':
            model = TD3.load(path_to_model, env=env)
        case _:
            print('Algorithm not found')
            return

    obs = env.reset()[0]
    terminated = False
    truncated = False
    while not terminated and not truncated:
        action, _ = model.predict(obs)
        print(f'Action: {action}')
        obs, _, terminated, truncated, _ = env.step(action)


if __name__ == '__main__':
    # Usage - training
    # python train_test.py SimonARC-v0 A2C -t
    #
    # Usage - testing
    # python train_test.py SimonARC-v0 A2C -s models/A2C_25000.zip
    parser = argparse.ArgumentParser(description='Train or test model.')
    parser.add_argument('gymenv', help='Gymnasium environment i.e. SimonARC-v0')
    parser.add_argument('sb3_algo', help='StableBaseline3 RL algorithm i.e. A2C, PPO')
    parser.add_argument('-t', '--train', action='store_true')
    parser.add_argument('-s', '--test', metavar='path_to_model')
    args = parser.parse_args()

    if args.train:
        gymenv = gym.make(args.gymenv)
        train(gymenv, args.sb3_algo)

    if args.test:
        if os.path.isfile(args.test):
            gymenv = gym.make(args.gymenv, render_mode='human')
            test(gymenv, args.sb3_algo, path_to_model=args.test)
        else:
            print(f'{args.test} not found.')

