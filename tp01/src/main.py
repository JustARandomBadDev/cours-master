import time

from pathlib import Path
from typing import cast

from camera import Camera
from renderer import Renderer
from skeleton import Skeleton
from tsv_parser import SkeletonFrame, TsvParser
from tsv_scraper import download_tsv


INDEX_URL_TSV = "https://share-irisa.univ-ubs.fr/mocap/pub/b8f0-9d51-798e-8c2c-f936-a32a-2687-fab0/MiS/TSV/"
DOWNLOAD_DIR_TSV = Path("assets/tsv")

WIDTH = 1280
HEIGHT = 720
FPS = 200.0


if __name__ == "__main__":
    download_tsv(
        INDEX_URL_TSV,
        DOWNLOAD_DIR_TSV,
    )

    skeleton_files = [
        path
        for path in sorted(DOWNLOAD_DIR_TSV.glob("*.tsv"))
        if "_s_" in path.stem
    ]

    if not skeleton_files:
        raise RuntimeError("No skeleton TSV file found.")

    path = skeleton_files[0]
    print(f"Playing {path.name}")

    parser = TsvParser(path)

    if not parser.is_skeleton:
        raise RuntimeError("The selected TSV is not a skeleton file.")

    frames = cast(
        list[SkeletonFrame],
        parser.parse(),
    )

    skeleton = Skeleton(frames)

    renderer = Renderer(
        WIDTH,
        HEIGHT,
        Path("assets/shaders/vert.glsl"),
        Path("assets/shaders/frag.glsl"),
        23 * 8 * 6 * 4,
    )

    camera = Camera(
        WIDTH,
        HEIGHT,
    )

    renderer.updateUniform(
        camera.getModel(),
        camera.getProjection(),
        camera.getView(),
    )

    start_time = time.perf_counter()

    while not renderer.shouldClose():
        elapsed = time.perf_counter() - start_time

        frame_index = (
            int(elapsed * FPS)
            % skeleton.getFrameCount()
        )

        vertices, indices = skeleton.buildMesh(
            frame_index
        )

        renderer.updateBuffer(
            vertices,
            indices,
        )

        renderer.render()

    renderer.cleanup()
