import numpy as np


def shoulder_tension(positions: np.ndarray, bones: list[str]) -> np.ndarray:
    hips = positions[:, bones.index("Hips")]
    neck = positions[:, bones.index("Neck")]
    left_shoulder = positions[:, bones.index("LeftShoulder")]
    right_shoulder = positions[:, bones.index("RightShoulder")]

    shoulder_height = (left_shoulder[:, 2] + right_shoulder[:, 2]) / 2.0
    shoulder_gap = np.abs(neck[:, 2] - shoulder_height)
    torso_length = np.linalg.norm(neck - hips, axis=1)

    return np.clip(
        1.0 - shoulder_gap / (0.25 * np.maximum(torso_length, 1e-9)),
        0.0,
        1.0,
    )


def back_tension(positions: np.ndarray, bones: list[str]) -> np.ndarray:
    hips = positions[:, bones.index("Hips")]
    spine1 = positions[:, bones.index("Spine1")]
    neck = positions[:, bones.index("Neck")]

    lower_back = spine1 - hips
    upper_back = neck - spine1
    lengths = (
        np.linalg.norm(lower_back, axis=1)
        * np.linalg.norm(upper_back, axis=1)
    )
    cosine = np.sum(lower_back * upper_back, axis=1) / np.maximum(lengths, 1e-9)
    angle = np.arccos(np.clip(cosine, -1.0, 1.0))

    return np.clip(angle / np.deg2rad(45.0), 0.0, 1.0)


def lower_body_tension(positions: np.ndarray, bones: list[str]) -> np.ndarray:
    knee_scores = []
    ankle_scores = []

    for side in ["Left", "Right"]:
        hip = positions[:, bones.index(f"{side}UpLeg")]
        knee = positions[:, bones.index(f"{side}Leg")]
        ankle = positions[:, bones.index(f"{side}Foot")]
        toes = positions[:, bones.index(f"{side}ToeBase")]

        thigh = hip - knee
        shin = ankle - knee
        lengths = np.linalg.norm(thigh, axis=1) * np.linalg.norm(shin, axis=1)
        cosine = np.sum(thigh * shin, axis=1) / np.maximum(lengths, 1e-9)
        knee_angle = np.arccos(np.clip(cosine, -1.0, 1.0))
        knee_scores.append(np.clip(
            (np.pi - knee_angle) / np.deg2rad(90.0),
            0.0,
            1.0,
        ))

        lower_leg = knee - ankle
        foot = toes - ankle
        lengths = np.linalg.norm(lower_leg, axis=1) * np.linalg.norm(foot, axis=1)
        cosine = np.sum(lower_leg * foot, axis=1) / np.maximum(lengths, 1e-9)
        ankle_angle = np.arccos(np.clip(cosine, -1.0, 1.0))
        ankle_scores.append(np.clip(
            (ankle_angle - np.deg2rad(120.0)) / np.deg2rad(30.0),
            0.0,
            1.0,
        ))

    knees = np.mean(knee_scores, axis=0)
    ankles = np.mean(ankle_scores, axis=0)

    return 0.5 * knees + 0.5 * ankles


def tension_scores(
    positions: np.ndarray,
    bones: list[str],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    shoulders = shoulder_tension(positions, bones)
    back = back_tension(positions, bones)
    lower_body = lower_body_tension(positions, bones)
    tension = (shoulders + back + lower_body) / 3.0

    return shoulders, back, lower_body, tension
