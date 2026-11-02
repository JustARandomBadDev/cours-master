BONES: list[tuple[str, str]] = [
    ("Hips", "Spine"),
    ("Spine", "Spine1"),
    ("Spine1", "Spine2"),
    ("Spine2", "Neck"),
    ("Neck", "Head"),

    ("Spine2", "LeftShoulder"),
    ("LeftShoulder", "LeftArm"),
    ("LeftArm", "LeftForeArm"),
    ("LeftForeArm", "LeftForeArmRoll"),
    ("LeftForeArmRoll", "LeftHand"),

    ("Spine2", "RightShoulder"),
    ("RightShoulder", "RightArm"),
    ("RightArm", "RightForeArm"),
    ("RightForeArm", "RightForeArmRoll"),
    ("RightForeArmRoll", "RightHand"),

    ("Hips", "LeftUpLeg"),
    ("LeftUpLeg", "LeftLeg"),
    ("LeftLeg", "LeftFoot"),
    ("LeftFoot", "LeftToeBase"),

    ("Hips", "RightUpLeg"),
    ("RightUpLeg", "RightLeg"),
    ("RightLeg", "RightFoot"),
    ("RightFoot", "RightToeBase"),
]
