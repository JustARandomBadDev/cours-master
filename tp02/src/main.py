from collections import Counter
from pathlib import Path
from sys import argv

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from tsv_parser import MarkerFrame, TsvParser

Segment = tuple[str, str, list[MarkerFrame]]

def load_segments(data_dir: Path) -> list[Segment]:
    segments: list[Segment] = []

    for path in sorted(data_dir.glob("*.csv")):
        parts = path.stem.split("_", 4)
        hand = parts[0]
        label = parts[4]
        frames = TsvParser(path).parse()
        segments.append((hand, label, frames))

    return segments

def print_statistics(segments: list[Segment]) -> None:
    segment_labels = Counter(label for _, label, _ in segments)
    frame_labels = Counter()
    hands = Counter()

    for hand, label, frames in segments:
        frame_labels[label] += len(frames)
        hands[hand] += 1

    print(f"segments: {len(segments)}")
    print(f"frames: {sum(len(frames) for _, _, frames in segments)}")
    print(f"hands: {dict(hands)}")
    print(f"segments per label: {dict(segment_labels)}")
    print(f"frames per label: {dict(frame_labels)}")

def extract_features(frames: list[MarkerFrame]) -> np.ndarray:
    features = []

    for frame in frames:
        joints = np.array(list(frame.values()))
        wrist = joints[0]
        features.append(np.linalg.norm(joints[1:] - wrist, axis=1))

    return np.array(features)

def build_xy(segments: list[Segment]) -> tuple[np.ndarray, np.ndarray]:
    x = []
    y = []

    for _, label, frames in segments:
        x.append(extract_features(frames))
        y.extend([label] * len(frames))

    return np.vstack(x), np.array(y)

def run_classifiers(x: np.ndarray, y: np.ndarray) -> None:
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    classifiers = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "K-NN": KNeighborsClassifier(),
        "Naive Bayes": GaussianNB(),
        "SVM": SVC(),
    }

    figure, axes = plt.subplots(2, 2, figsize=(14, 12))

    for axis, (name, classifier) in zip(axes.flat, classifiers.items()):
        classifier.fit(x_train, y_train)
        prediction = classifier.predict(x_test)

        print(f"\n{name}")
        print(f"accuracy: {accuracy_score(y_test, prediction):.4f}")
        print(f"precision: {precision_score(y_test, prediction, average='weighted', zero_division=0):.4f}")
        print(f"recall: {recall_score(y_test, prediction, average='weighted', zero_division=0):.4f}")
        print(f"f1: {f1_score(y_test, prediction, average='weighted', zero_division=0):.4f}")

        ConfusionMatrixDisplay.from_predictions(
            y_test,
            prediction,
            ax=axis,
            xticks_rotation=90,
            colorbar=False,
        )
        axis.set_title(name)

    figure.tight_layout()
    figure.savefig("confusion_matrices.png")

def main() -> None:
    data_dir = Path(argv[1]) if len(argv) > 1 else Path("data")
    segments = load_segments(data_dir)
    print_statistics(segments)
    x, y = build_xy(segments)
    run_classifiers(x, y)

if __name__ == "__main__":
    main()
