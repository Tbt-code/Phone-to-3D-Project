from pathlib import Path
from src.config import DATA_DIR
from src.pipeline.video_to_frames import extract_frames
from src.pipeline.run_colmap import run_colmap
from src.utils.file_utils import ensure_dir
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)


def run_full_pipeline(video_path: str, output_name: str = "output") -> Path:
    video = Path(video_path)
    frames_dir = ensure_dir(DATA_DIR / "frames" / output_name)
    workspace_dir = ensure_dir(DATA_DIR / "colmap" / output_name)

    logger.info("=== Step 1: Extract frames ===")
    count = extract_frames(str(video), frames_dir)
    if count == 0:
        raise RuntimeError("No frames extracted — check the video file.")

    logger.info("=== Step 2: COLMAP SfM reconstruction ===")
    sparse_dir = run_colmap(frames_dir, workspace_dir)

    ply_path = sparse_dir / "0" / "points3D.ply"
    logger.info(f"=== Pipeline complete. Point cloud: {ply_path} ===")
    return ply_path
