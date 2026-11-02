import numpy as np

from bones import BONES
from tsv_parser import SkeletonFrame


class Skeleton:
    def __init__(self, p_frames: list[SkeletonFrame]) -> None:
        if not p_frames:
            raise ValueError("Skeleton requires at least one frame.")

        self.__frames = p_frames

    def getFrameCount(self) -> int:
        return len(self.__frames)

    def buildMesh(
        self,
        p_frame_index: int,
    ) -> tuple[np.ndarray, np.ndarray]:
        frame = self.__frames[p_frame_index]

        vertices: list[float] = []
        indices: list[int] = []

        hips = np.array(frame["Hips"][0], dtype=np.float32)

        for parent, child in BONES:
            start = self.__getPosition(frame, parent, hips)
            end = self.__getPosition(frame, child, hips)

            self.__addBone(
                vertices,
                indices,
                start,
                end,
            )

        return (
            np.array(vertices, dtype="f4"),
            np.array(indices, dtype="u4"),
        )

    def __getPosition(
        self,
        p_frame: SkeletonFrame,
        p_bone: str,
        p_hips: np.ndarray,
    ) -> np.ndarray:
        position = np.array(
            p_frame[p_bone][0],
            dtype=np.float32,
        )

        position = (position - p_hips) / 1000.0

        return position[[0, 2, 1]]

    def __addBone(
        self,
        p_vertices: list[float],
        p_indices: list[int],
        p_start: np.ndarray,
        p_end: np.ndarray,
    ) -> None:
        direction = p_end - p_start
        length = np.linalg.norm(direction)

        if length == 0.0:
            return

        direction /= length

        up = np.array(
            [0.0, 1.0, 0.0],
            dtype=np.float32,
        )

        if abs(np.dot(direction, up)) > 0.9:
            up = np.array(
                [1.0, 0.0, 0.0],
                dtype=np.float32,
            )

        side = np.cross(direction, up)
        side /= np.linalg.norm(side)
        side *= 0.015

        up = np.cross(side, direction)
        up /= np.linalg.norm(up)
        up *= 0.015

        corners = [
            p_start - side - up,
            p_start + side - up,
            p_start + side + up,
            p_start - side + up,
            p_end - side - up,
            p_end + side - up,
            p_end + side + up,
            p_end - side + up,
        ]

        first = len(p_vertices) // 6

        for position in corners:
            p_vertices.extend([
                float(position[0]),
                float(position[1]),
                float(position[2]),
                0.2,
                0.75,
                1.0,
            ])

        p_indices.extend([
            first + 0, first + 1, first + 2,
            first + 2, first + 3, first + 0,

            first + 4, first + 6, first + 5,
            first + 6, first + 4, first + 7,

            first + 0, first + 4, first + 5,
            first + 5, first + 1, first + 0,

            first + 1, first + 5, first + 6,
            first + 6, first + 2, first + 1,

            first + 2, first + 6, first + 7,
            first + 7, first + 3, first + 2,

            first + 3, first + 7, first + 4,
            first + 4, first + 0, first + 3,
        ])
