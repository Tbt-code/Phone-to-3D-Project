from pathlib import Path
from src.config import DATA_DIR
from src.pipeline.video_to_frames import extract_frames
from src.pipeline.run_colmap import run_colmap
from src.pipeline.run_openmvs import run_openmvs  # Integrated the newly created OpenMVS module
from src.utils.file_utils import ensure_dir
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def run_full_pipeline(input_path: str, output_name: str = "gerard_hall", is_video: bool = False) -> Path:
    """
    End-to-end 3D Reconstruction Pipeline.
    If is_video=False, it processes the image folder directly (ideal for static datasets like Gerard Hall).
    """
    workspace_dir = ensure_dir(DATA_DIR / "colmap" / output_name)
    frames_dir = ensure_dir(DATA_DIR / "frames" / output_name)

    # === Step 1: Input Handling (Video Processing or Direct Image Dataset) ===
    if is_video:
        logger.info("=== Step 1: Extracting frames from video ===")
        count = extract_frames(input_path, frames_dir)
        if count == 0:
            raise RuntimeError("No frames extracted — check the video file.")
        image_input_dir = frames_dir
    else:
        logger.info("=== Step 1: Using direct image dataset (Skipping FFmpeg) ===")
        image_input_dir = Path(input_path)
        if not image_input_dir.exists():
            raise FileNotFoundError(f"Image directory not found: {input_path}")

    # === Step 2: COLMAP SfM reconstruction ===
    logger.info("=== Step 2: COLMAP SfM reconstruction starting ===")
    sparse_dir = run_colmap(image_input_dir, workspace_dir)

    # === Step 3: OpenMVS Integration (Format conversion, geo.dmap optimization, and Mesh generation) ===
    logger.info("=== Step 3: OpenMVS Dense Reconstruction & Mesh Generation starting ===")
    mesh_ply_path = run_openmvs(workspace_dir, sparse_dir, image_input_dir)

    logger.info(f"=== PIPELINE SUCCESSFUL! Final Mesh PLY: {mesh_ply_path} ===")
    return mesh_ply_path