import re
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from stats import compute_descriptors
from tension import tension_scores


TSV_DIR = Path("assets/tsv")
PLOT_DIR = Path("assets/plots")

LABELS = {
    "speed": ("Vitesse", "m/s"),
    "acceleration": ("Accélération", "m/s²"),
    "jerk": ("Jerk", "m/s³"),
    "quantity_of_motion": ("Quantité de mouvement", "m/s"),
    "centroid_speed": ("Vitesse du centroïde", "m/s"),
    "bounding_box_volume": ("Volume englobant", "m³"),
}


def file_info(path: Path) -> tuple[str, str | None]:
    match = re.search(r"_(\d+)a_", path.stem)
    subject = path.stem[:match.start()].replace("_", " ")
    subject = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", subject)
    name = path.stem.lower()
    movement = None

    if "marche" in name:
        for word, label in [("lente", "Lente"), ("normale", "Normale"), ("rapide", "Rapide")]:
            if word in name:
                movement = label

    return f"{subject} ({match.group(1)} ans)", movement


def load_data() -> tuple[list[dict], dict]:
    records = []
    representative = None

    for path in sorted(TSV_DIR.glob("*_s_*.tsv")):
        bones, positions, frequency, descriptors = compute_descriptors(path)
        shoulders, back, lower_body, tension = tension_scores(positions, bones)
        subject, movement = file_info(path)
        record = {
            "subject": subject,
            "movement": movement,
            "tension": np.mean(tension),
        }
        records.append(record)

        if representative is None and record["movement"] == "Normale":
            representative = {
                "bones": bones,
                "positions": positions,
                "frequency": frequency,
                "descriptors": descriptors,
                "shoulders": shoulders,
                "back": back,
                "lower_body": lower_body,
                "tension": tension,
            }

    return records, representative


def plot_descriptors(data: dict) -> None:
    time = np.arange(len(data["tension"])) / data["frequency"]
    figure, axes = plt.subplots(3, 2, figsize=(11, 8), sharex=True)

    for axis, (name, (label, unit)) in zip(axes.flat, LABELS.items()):
        axis.plot(time, data["descriptors"][name], linewidth=0.8)
        axis.set_title(label)
        axis.set_ylabel(unit)
        axis.grid(alpha=0.25)

    axes[-1, 0].set_xlabel("Temps (s)")
    axes[-1, 1].set_xlabel("Temps (s)")
    figure.tight_layout()
    figure.savefig(PLOT_DIR / "descripteurs_temps.png", dpi=150)
    plt.close(figure)


def plot_tension(data: dict) -> None:
    frequency = data["frequency"]
    tension = data["tension"]
    time = np.arange(len(tension)) / frequency
    size = int(frequency)
    tension_windows = [np.mean(tension[i:i + size]) for i in range(0, len(tension), size)]
    figure, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(time, data["shoulders"], linewidth=0.7, label="Épaules")
    axes[0].plot(time, data["back"], linewidth=0.7, label="Dos")
    axes[0].plot(time, data["lower_body"], linewidth=0.7, label="Bas du corps")
    axes[0].plot(time, tension, linewidth=1.0, label="Tension")
    axes[0].axhline(np.mean(tension), color="black", linestyle="--", label="Séquence")
    axes[0].set_xlabel("Temps (s)")
    axes[0].set_ylabel("Score")
    axes[1].bar(range(len(tension_windows)), tension_windows)
    axes[1].set_xlabel("Fenêtre de 1 s")
    axes[1].set_ylabel("Tension moyenne")

    for axis in axes.flat:
        axis.grid(alpha=0.25)
        if axis.get_legend_handles_labels()[0]:
            axis.legend()

    axes[0].set_title("Tension par frame")
    axes[1].set_title("Tension par fenêtre")
    figure.tight_layout()
    figure.savefig(PLOT_DIR / "tension_temps.png", dpi=150)
    plt.close(figure)


def plot_subjects(records: list[dict]) -> None:
    records = [record for record in records if record["movement"]]
    subjects = sorted({record["subject"] for record in records})
    figure, axis = plt.subplots(figsize=(13, 5))
    x = np.arange(len(subjects))
    selected = [[record for record in records if record["subject"] == subject] for subject in subjects]
    axis.bar(x, [np.mean([record["tension"] for record in values]) for values in selected])
    axis.set_ylabel("Tension globale")
    axis.set_xticks(x, subjects, rotation=35, ha="right")
    axis.grid(axis="y", alpha=0.25)

    figure.tight_layout()
    figure.savefig(PLOT_DIR / "comparaison_sujets.png", dpi=150)
    plt.close(figure)


def plot_trajectory(data: dict) -> None:
    bones = data["bones"]
    positions = data["positions"]
    trajectory = positions[:, bones.index("RightHand")] - positions[:, bones.index("Hips")]
    figure = plt.figure(figsize=(7, 6))
    axis = figure.add_subplot(111, projection="3d")
    axis.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], linewidth=0.8)
    axis.set_xlabel("X (m)")
    axis.set_ylabel("Y (m)")
    axis.set_zlabel("Z (m)")
    axis.set_title("Trajectoire de la main droite par rapport au bassin")
    figure.tight_layout()
    figure.savefig(PLOT_DIR / "trajectoire_main_3d.png", dpi=150)
    plt.close(figure)


def print_summary(records: list[dict], data: dict) -> None:
    print("Séquence représentative : Aline Larboulette, marche normale")
    print("descripteur                 moyenne        min        max    médiane")

    for name, values in data["descriptors"].items():
        print(f"{name:25} {np.mean(values):10.4g} {np.min(values):10.4g} {np.max(values):10.4g} {np.median(values):10.4g}")

    tension = data["tension"]
    size = int(data["frequency"])
    windows = [np.mean(tension[i:i + size]) for i in range(0, len(tension), size)]
    print(f"\nComposantes moyennes: épaules {np.mean(data['shoulders']):.4g}, dos {np.mean(data['back']):.4g}, bas du corps {np.mean(data['lower_body']):.4g}")
    print(f"Tension par frame  : moyenne {np.mean(tension):.4g}, min {np.min(tension):.4g}, max {np.max(tension):.4g}, médiane {np.median(tension):.4g}")
    print(f"Tension par seconde: moyenne {np.mean(windows):.4g}, min {np.min(windows):.4g}, max {np.max(windows):.4g}, médiane {np.median(windows):.4g}")
    print(f"Valeurs globales de tension calculées pour {len(records)} séquences.")


if __name__ == "__main__":
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    records, representative = load_data()
    plot_descriptors(representative)
    plot_tension(representative)
    plot_subjects(records)
    plot_trajectory(representative)
    print_summary(records, representative)
