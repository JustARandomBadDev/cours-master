import urllib.request

from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def download_tsv(url: str, dir: Path) -> None:
    with urllib.request.urlopen(url) as response:
        soup: BeautifulSoup = BeautifulSoup(response.read(), "html.parser")

    file_urls: set[str] = {
        urljoin(url, link["href"])                              # type: ignore
        for link in soup.find_all("a", href=True)
        if urlparse(link["href"]).path.lower().endswith(".tsv") # type: ignore
        or urlparse(link["href"]).path.lower().endswith(".mp4") # type: ignore
    }

    dir.mkdir(parents=True, exist_ok=True)

    print(f"{len(file_urls)} found.")

    for file_url in sorted(file_urls):
        filename: str = Path(urlparse(file_url).path).name
        destination: Path = dir / filename

        if destination.exists():
            print(f"Already exist : {filename}")
            continue

        print(f"Download : {filename}")
        urllib.request.urlretrieve(file_url, destination)

if __name__ == "__main__":
    download_tsv(
        "https://share-irisa.univ-ubs.fr/mocap/pub/b8f0-9d51-798e-8c2c-f936-a32a-2687-fab0/MiS/TSV/",
        Path("assets/tsv"),
    )
