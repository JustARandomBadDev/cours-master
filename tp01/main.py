#!/usr/bin/python3

import urllib.request

from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from typing import Dict, List, Tuple

MarkerData = Tuple[float, float, float]
Frame = Dict[str, MarkerData]

INDEX_URL_TSV = "https://share-irisa.univ-ubs.fr/mocap/pub/b8f0-9d51-798e-8c2c-f936-a32a-2687-fab0/MiS/TSV/"
DOWNLOAD_DIR_TSV = Path("tsv")

INDEX_URL_MP4 = "https://share-irisa.univ-ubs.fr/mocap/pub/b8f0-9d51-798e-8c2c-f936-a32a-2687-fab0/MiS/Animated/"
DOWNLOAD_DIR_MP4 = Path("mp4")


def download_files(url: str, dir: Path) -> None:
    with urllib.request.urlopen(url) as response:
        soup: BeautifulSoup = BeautifulSoup(response.read(), "html.parser")

    file_urls: set[str] = {
        urljoin(url, link["href"])                              # type: ignore
        for link in soup.find_all("a", href=True)
        if urlparse(link["href"]).path.lower().endswith(".tsv") # type: ignore
        or urlparse(link["href"]).path.lower().endswith(".mp4") # type: ignore
    }

    dir.mkdir(exist_ok=True)

    print(f"{len(file_urls)} found.")

    for file_url in sorted(file_urls):
        filename: str = Path(urlparse(file_url).path).name
        destination: Path = dir / filename

        if destination.exists():
            print(f"Already exist : {filename}")
            continue

        print(f"Download : {filename}")
        urllib.request.urlretrieve(file_url, destination)


def parse_tsv(path: str) -> List[Frame]:
    with open(path, "r") as f:
        lines: List[str] = f.readlines()

    header: List[str] = lines[11].strip().split("\t")

    markers: List[str] = [
        header[i].removesuffix(" X")
        for i in range(0, len(header), 3)
    ]

    frames: List[Frame] = []

    for line in lines[12:]:
        values: List[str] = line.strip().split("\t")
        frame: Frame = {}

        for i, marker in enumerate(markers):
            start: int = i * 3

            data: MarkerData = (
                float(values[start]),
                float(values[start + 1]),
                float(values[start + 2])
            )

            frame[marker] = data

        frames.append(frame)

    return frames


def average_position(
    frames: List[Frame],
    markers: List[str]
) -> Tuple[float, float, float]:
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

    return x / count, y / count, z / count


if __name__ == "__main__":
    download_files(INDEX_URL_TSV, DOWNLOAD_DIR_TSV)
    download_files(INDEX_URL_MP4, DOWNLOAD_DIR_MP4)

    tsv_files = "tsv/AugustinGerard_11a_Marche_Normale_880_2580.tsv"
    
    data: List[Frame] = parse_tsv(tsv_files)
    
    result = average_position(data, ["HeadL"])
    print(f"Average HeadL position in full motion : {result}")
    
    upper_body_markers = ["HeadL", "HeadTop", "HeadR", "HeadFront", "LShoulderBack", "LShoulderTop", "RShoulderTop", "RShoulderBack", "SpineTop", "Chest", "BackL", "BackR", "LElbowOut", "LElbowBack", "RElbowOut", "RElbowBack", "LWristOut", "LWristIn", "LHandOut", "RWristOut", "RWristIn", "RHandOut", "LThumb", "LForeFinger", "LMiddleFinger", "LRingFinger", "LLittleFinger", "RThumb", "RForeFinger", "RMiddleFinger", "RRingFinger", "RLittleFinger"]
    
    result = average_position(data, upper_body_markers)
    print(f"Average upper body position in full motion : {result}")