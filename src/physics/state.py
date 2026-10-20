from typing import Literal, TypeAlias

import numpy as np

Vec2: TypeAlias = np.ndarray[tuple[Literal[2]], np.dtype[np.float64]]


class Stone:
    mass: float
    position: Vec2
    velocity: Vec2

    def __init__(self, mass: float, position: Vec2, velocity: Vec2):
        self.mass = mass
        self.position = position
        self.velocity = velocity

    def to_vector(self) -> np.ndarray:
        return np.concatenate(
            [
                self.position,
                self.velocity,
            ]
        )
