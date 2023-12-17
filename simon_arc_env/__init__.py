from .simon_arc_env import SimonARCEnv

from gymnasium.envs.registration import register

__all__ = [SimonARCEnv]

register(id="SimonARC-v0", entry_point="simon_arc_env:SimonARCEnv")
