import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

if sys.platform == "win32":
    FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
    OPENMVS_BIN = "C:/OpenMVS/bin"
else:
    FFMPEG_PATH = "ffmpeg"
    OPENMVS_BIN = "/usr/local/bin"

COLMAP_PATH = "colmap"

FRAME_RATE = 2
