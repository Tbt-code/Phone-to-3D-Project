import sys
from pathlib import Path

# Automatically resolves the absolute path to the project's root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Standardized data directory path
DATA_DIR = PROJECT_ROOT / "data"

if sys.platform == "win32":
    # Global binary paths configured for Windows environment
    FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
    COLMAP_PATH = r"C:\COLMAP\COLMAP.bat"
    
    # Dynamically maps OpenMVS binaries to the root directory where your .exe files reside
    OPENMVS_BIN = str(PROJECT_ROOT)
else:
    # Standard fallback binary names for Unix/Linux environments
    FFMPEG_PATH = "ffmpeg"
    COLMAP_PATH = "colmap"
    OPENMVS_BIN = "/usr/local/bin"

# Frame extraction configuration for the video preprocessing module
FRAME_RATE = 10