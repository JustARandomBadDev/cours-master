from pathlib import Path
from typing import cast

import numpy as np

from tsv_parser import SkeletonFrame, TsvParser


TSV_DIR = Path("assets/tsv")


def get_frequency(path: Path) -> float:
    file = open(path, "r")

    for line in file:
        if line.startswith("FREQUENCY"):
            return float(line.split("\t")[1])

    return 0.0


def compute_stats(path: Path) -> None:
    parser = TsvParser(path)
    frames = cast(list[SkeletonFrame], parser.parse())

    bones = list(frames[0].keys())

    positions = np.array([
        [frame[bone][0] for bone in bones]
        for frame in frames
    ]) / 1000.0

    frequency = get_frequency(path)
    dt = 1.0 / frequency

    velocity = np.gradient(positions, dt, axis=0)
    acceleration = np.gradient(velocity, dt, axis=0)
    jerk = np.gradient(acceleration, dt, axis=0)

    speed = np.linalg.norm(velocity, axis=2)
    acceleration = np.linalg.norm(acceleration, axis=2)
    jerk = np.linalg.norm(jerk, axis=2)

    centroid = np.mean(positions, axis=1)
    centroid_velocity = np.gradient(centroid, dt, axis=0)
    centroid_speed = np.linalg.norm(centroid_velocity, axis=1)

    minimum = np.min(positions, axis=1)
    maximum = np.max(positions, axis=1)

    bounding_box_volume = np.prod(
        maximum - minimum,
        axis=1
    )

    descriptors = {
        "speed": np.mean(speed, axis=1),
        "acceleration": np.mean(acceleration, axis=1),
        "jerk": np.mean(jerk, axis=1),

        "quantity_of_motion": np.sum(speed, axis=1),
        "centroid_speed": centroid_speed,
        "bounding_box_volume": bounding_box_volume,
    }

    print()
    print(path.stem)

    for name, values in descriptors.items():
        print(name)
        print("  mean   :", np.mean(values))
        print("  min    :", np.min(values))
        print("  max    :", np.max(values))
        print("  median :", np.median(values))


if __name__ == "__main__":
    files = [
        path
        for path in TSV_DIR.glob("*.tsv")
        if "_s_" in path.stem
    ]

    for path in files:
        compute_stats(path)