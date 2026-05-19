import subprocess
from pathlib import Path
from src.config import FRAME_RATE, FFMPEG_PATH
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def extract_frames(video_path: str, output_dir: Path) -> int:
    video = Path(video_path)
    if not video.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        FFMPEG_PATH,
        "-i", str(video),
        "-vf", f"fps={FRAME_RATE}",
        "-q:v", "2",
        str(output_dir / "frame_%04d.jpg"),
        "-y",
    ]

    logger.info(f"Extracting frames from: {video_path}")
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise RuntimeError(f"FFmpeg not found at '{FFMPEG_PATH}'. Install with: brew install ffmpeg")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg failed: {e}")

    frames = list(output_dir.glob("frame_*.jpg"))
    logger.info(f"Extracted {len(frames)} frames → {output_dir}")
    return len(frames)
