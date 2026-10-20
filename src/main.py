import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.physics.scenarios import SCENARIOS, find_scenario
from src.visualizer import run

EXPERIMENT = {
    "v0": 20.0,
    "angle": 45.0,
    "mass": 1.0,
    "k": 0.1,
    "model": "viscous",
    "rtol": 1e-6,
    "atol": 1e-9,
}


def scenario_params(scenario):
    vx, vy = scenario.stone.velocity
    return {
        **EXPERIMENT,
        "v0": math.hypot(vx, vy),
        "angle": math.degrees(math.atan2(vy, vx)),
        "mass": scenario.stone.mass,
        "k": scenario.c,
        "model": scenario.choice,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        run(**EXPERIMENT)
    elif scenario := find_scenario(sys.argv[1]):
        run(**scenario_params(scenario))
    else:
        print("Нет такого сценария. Доступные:")
        for s in SCENARIOS:
            print(f'  "{s.name}"')
