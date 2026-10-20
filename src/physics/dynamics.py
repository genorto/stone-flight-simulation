from types import FunctionType

import numpy as np

from src.physics import forces, state


def set_choise(choise: str) -> FunctionType:
    def dynamic(
        t: float,
        vector: np.ndarray,
        mass: float,
        c: float,
        g: float,
    ) -> np.ndarray:
        position: state.Vec2 = vector[:2]
        velocity: state.Vec2 = vector[2:]
        friction = forces.friction_types[choise]
        stone = state.Stone(mass, position, velocity)

        gravity = forces.gravity(stone, g)
        friction_force = friction(stone, c)
        a = (gravity + friction_force) / stone.mass

        return np.concatenate([velocity, a])

    return dynamic
