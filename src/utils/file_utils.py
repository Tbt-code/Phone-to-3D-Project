import shutil
from pathlib import Path


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def clear_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def list_images(directory: Path, extensions: tuple = (".jpg", ".jpeg", ".png")) -> list[Path]:
    return sorted(f for f in directory.iterdir() if f.suffix.lower() in extensions)
