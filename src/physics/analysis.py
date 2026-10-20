import math
from dataclasses import dataclass

import numpy as np

from src.physics.scenarios import Scenario

EPSILON = 1e-12


@dataclass(frozen=True)
class CalcErrorResult:
    position_error: np.ndarray
    relative_position_error: np.ndarray


def calc_position(scenario: Scenario, t: float) -> tuple[float, float]:
    coeff = scenario.c / scenario.stone.mass

    t = t - scenario.t_span[0]

    if scenario.c == 0:
        stone = scenario.stone
        return (
            stone.position[0] + stone.velocity[0] * t,
            stone.position[1] + stone.velocity[1] * t - scenario.g * t**2 / 2,
        )

    def x(t: float) -> float:
        return scenario.stone.position[0] + scenario.stone.velocity[0] / coeff * (
            1 - math.exp(-coeff * t)
        )

    def y(t: float) -> float:
        return (
            scenario.stone.position[1]
            + (scenario.stone.velocity[1] + scenario.g / coeff) / coeff * (1 - math.exp(-coeff * t))
            - scenario.g / coeff * t
        )

    return (x(t), y(t))


"""
def calc_velocity(scenario: Scenario) -> tuple[float, float]:
    coeff = scenario.c / scenario.stone.mass
    def vx(t: float) -> float:
        return scenario.stone.velocity[0] * math.exp(-coeff * t)

    def vy(t: float) -> float:
        return (scenario.stone.velocity[1] + scenario.g / coeff) * math.exp(
            -coeff * t
        ) - scenario.g / coeff * t

    return tuple(vx(scenario.t_span[1]), vy(scenario.t_span[1]))
"""


def calc_errors(y: np.ndarray, t: np.ndarray, scenario: Scenario) -> CalcErrorResult:
    position_error = []
    relative_position_error = []
    if scenario.choice == "viscous":
        for time, pos in zip(t, y.T):
            x_int, y_int, vx_int, vy_int = pos
            x_pos, y_pos = calc_position(scenario, time)
            position_error.append(
                np.linalg.norm(np.array([abs(x_pos - x_int), abs(y_pos - y_int)]))
            )
            relative_position_error.append(
                np.linalg.norm(
                    np.array(
                        [
                            abs(x_pos - x_int) / max(abs(x_int), EPSILON),
                            abs(y_pos - y_int) / max(abs(y_int), EPSILON),
                        ]
                    )
                )
            )

    return CalcErrorResult(np.array(position_error), np.array(relative_position_error))
