import numpy as np

from src.physics.state import Stone, Vec2


def gravity(stone: Stone, g: float) -> Vec2:
    return np.array([0.0, -stone.mass * g], dtype=np.float64)


def viscous_friction(stone: Stone, c: float) -> Vec2:
    return -stone.velocity * c


def head_on_friction(stone: Stone, c: float) -> Vec2:
    return -np.linalg.norm(stone.velocity) * c * stone.velocity


friction_types = {
    "viscous": viscous_friction,
    "head_on": head_on_friction,
}
