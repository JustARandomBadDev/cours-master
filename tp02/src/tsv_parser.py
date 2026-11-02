from pathlib import Path
from typing import Dict, List, Tuple


Position = Tuple[float, float, float]
MarkerFrame = Dict[str, Position]


class TsvParser:
    def __init__(self, path: str | Path) -> None:
        self.__path = Path(path)

    def parse(self) -> List[MarkerFrame]:
        with open(self.__path, "r") as f:
            lines: List[str] = f.readlines()

        return self.__parse_markers(lines)

    def __parse_markers(self, lines: List[str]) -> List[MarkerFrame]:
        header: List[str] = lines[0].strip().split()

        markers: List[str] = [
            header[i].removesuffix("_x")
            for i in range(0, len(header), 3)
        ]

        frames: List[MarkerFrame] = []

        for line in lines[1:]:
            values: List[str] = line.strip().split()
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
