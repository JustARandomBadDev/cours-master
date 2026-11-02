from pathlib import Path
from typing import Dict, List, Tuple


Position = Tuple[float, float, float]
Quaternion = Tuple[float, float, float, float]

MarkerData = Position
SkeletonData = Tuple[Position, Quaternion]

MarkerFrame = Dict[str, MarkerData]
SkeletonFrame = Dict[str, SkeletonData]


class TsvParser:
    def __init__(self, path: str | Path) -> None:
        self.__path = Path(path)
        self.__is_skeleton = "_s_" in self.__path.stem

    @property
    def is_skeleton(self) -> bool:
        return self.__is_skeleton

    def parse(self) -> List[MarkerFrame] | List[SkeletonFrame]:
        with open(self.__path, "r") as f:
            lines: List[str] = f.readlines()

        if self.__is_skeleton:
            return self.__parse_skeleton(lines)

        return self.__parse_markers(lines)

    def __parse_markers(self, lines: List[str]) -> List[MarkerFrame]:
        header: List[str] = lines[11].strip().split("\t")

        markers: List[str] = [
            header[i].removesuffix(" X")
            for i in range(0, len(header), 3)
        ]

        frames: List[MarkerFrame] = []

        for line in lines[12:]:
            values: List[str] = line.strip().split("\t")
            frame: MarkerFrame = {}

            for i, marker in enumerate(markers):
                start: int = i * 3

                frame[marker] = (
                    float(values[start]),
                    float(values[start + 1]),
                    float(values[start + 2]),
                )

            frames.append(frame)

        return frames

    def __parse_skeleton(self, lines: List[str]) -> List[SkeletonFrame]:
        header: List[str] = lines[7].strip().split("\t")

        bones: List[str] = [
            header[i]
            for i in range(0, len(header), 8)
        ]

        frames: List[SkeletonFrame] = []

        for line in lines[8:]:
            values: List[str] = line.strip().split("\t")
            frame: SkeletonFrame = {}

            for i, bone in enumerate(bones):
                start: int = i * 8

                position: Position = (
                    float(values[start]),
                    float(values[start + 1]),
                    float(values[start + 2]),
                )

                quaternion: Quaternion = (
                    float(values[start + 3]),
                    float(values[start + 4]),
                    float(values[start + 5]),
                    float(values[start + 6]),
                )

                frame[bone] = (
                    position,
                    quaternion,
                )

            frames.append(frame)

        return frames

    @staticmethod
    def average_position(
        frames: List[MarkerFrame],
        markers: List[str],
    ) -> Position:
        x: float = 0.0
        y: float = 0.0
        z: float = 0.0
        count: int = 0

        for frame in frames:
            for marker in markers:
                x += frame[marker][0]
                y += frame[marker][1]
                z += frame[marker][2]
                count += 1

        return (
            x / count,
            y / count,
            z / count,
        )
