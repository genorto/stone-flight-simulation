from dataclasses import dataclass

import numpy as np

from src.physics.state import Stone

G = 9.80665

C_HEADON = 0.47
C_VISCOUS = 1.81e-5


@dataclass(frozen=True)
class Scenario:
    name: str
    stone: Stone
    t_span: tuple[float, float]
    choice: str = "viscous"
    c: float | None = None
    g: float = G

    def __post_init__(self):
        if self.c is None:
            object.__setattr__(
                self,
                "c",
                C_VISCOUS if self.choice == "viscous" else C_HEADON,
            )


SCENARIOS = [
    Scenario(
        name="Viscous: basic",
        stone=Stone(1.0, np.array([0.0, 0.0]), np.array([10.0, 15.0])),
        t_span=(0.0, 5.0),
        choice="viscous",
    ),
    Scenario(
        name="Viscous: heavy stone",
        stone=Stone(10.0, np.array([0.0, 0.0]), np.array([10.0, 15.0])),
        t_span=(0.0, 5.0),
        choice="viscous",
    ),
    Scenario(
        name="Viscous: light stone",
        stone=Stone(0.1, np.array([0.0, 0.0]), np.array([10.0, 15.0])),
        t_span=(0.0, 5.0),
        choice="viscous",
    ),
    Scenario(
        name="Viscous: high speed",
        stone=Stone(1.0, np.array([0.0, 0.0]), np.array([30.0, 40.0])),
        t_span=(0.0, 10.0),
        choice="viscous",
    ),
    Scenario(
        name="Viscous: strong resistance",
        stone=Stone(1.0, np.array([0.0, 0.0]), np.array([10.0, 15.0])),
        t_span=(0.0, 5.0),
        choice="viscous",
        c=C_VISCOUS * 10,
    ),
    Scenario(
        name="Headon: basic",
        stone=Stone(1.0, np.array([0.0, 0.0]), np.array([10.0, 15.0])),
        t_span=(0.0, 5.0),
        choice="head_on",
    ),
    Scenario(
        name="Headon: heavy stone",
        stone=Stone(10.0, np.array([0.0, 0.0]), np.array([10.0, 15.0])),
        t_span=(0.0, 5.0),
        choice="head_on",
    ),
    Scenario(
        name="Headon: light stone",
        stone=Stone(0.1, np.array([0.0, 0.0]), np.array([10.0, 15.0])),
        t_span=(0.0, 5.0),
        choice="head_on",
    ),
    Scenario(
        name="Headon: vertical throw",
        stone=Stone(1.0, np.array([0.0, 0.0]), np.array([0.0, 25.0])),
        t_span=(0.0, 8.0),
        choice="head_on",
    ),
    Scenario(
        name="Headon: strong resistance",
        stone=Stone(1.0, np.array([0.0, 20.0]), np.array([20.0, 10.0])),
        t_span=(0.0, 10.0),
        choice="head_on",
        c=C_HEADON * 10,
    ),
]


def find_scenario(name: str) -> Scenario | None:
    return next((scenario for scenario in SCENARIOS if scenario.name == name), None)
