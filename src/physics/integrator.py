from typing import Any

import numpy as np
from scipy import integrate

from src.physics.dynamics import set_choise
from src.physics.state import Stone


def hit_ground(t, position, *args):
    return position[1]


hit_ground.terminal = True
hit_ground.direction = -1


def integrator(
    friction_choise: str,
    c: float,
    g: float,
    stone: Stone,
    t_span: tuple[float, float],
    rtol: float,
    atol: float,
) -> tuple[
    np.ndarray[tuple[int], np.dtype[np.float64]],
    np.ndarray[tuple[int, int], np.dtype[Any]],
]:
    args = (stone.mass, c, g)

    rate = c / stone.mass
    if friction_choise == "head_on":
        rate = max(
            rate * np.linalg.norm(stone.velocity),
            np.sqrt(c * g / stone.mass),
        )
    max_step = 0.01 / rate if rate else np.inf

    sol = integrate.solve_ivp(
        set_choise(choise=friction_choise),
        t_span,
        stone.to_vector(),
        args=args,
        rtol=rtol,
        atol=atol,
        events=hit_ground,
        max_step=max_step,
    )

    if not sol.success:
        raise RuntimeError(sol.message)

    return sol.t, sol.y
