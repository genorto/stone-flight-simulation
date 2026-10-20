import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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

if __name__ == "__main__":
    run(**EXPERIMENT)
