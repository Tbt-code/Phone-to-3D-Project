import subprocess
from pathlib import Path
from src.config import COLMAP_PATH
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)


def run_colmap(image_dir: Path, workspace_dir: Path) -> Path:
    database = workspace_dir / "database.db"
    sparse_dir = workspace_dir / "sparse"
    sparse_dir.mkdir(parents=True, exist_ok=True)

    # --- Step 1: Feature Extraction ---
    _run(["feature_extractor",
          "--database_path", str(database),
          "--image_path", str(image_dir),
          "--ImageReader.single_camera", "1",
          "--SiftExtraction.max_num_features", "8192"])

    # --- Step 2: Feature Matching ---
    _run([
        "exhaustive_matcher",
        "--database_path", str(database)
    ])
    
    # --- Step 3: Sparse Reconstruction (Incremental Mapping) ---
    _run(["mapper",
          "--database_path", str(database),
          "--image_path", str(image_dir),
          "--output_path", str(sparse_dir),
          "--Mapper.init_min_num_inliers", "15",
          "--Mapper.abs_pose_min_num_inliers", "15",
          "--Mapper.min_num_matches", "10"])

    # --- Step 4: Export to Standard TXT format ---
    output_txt_dir = sparse_dir / "0_txt"
    output_txt_dir.mkdir(parents=True, exist_ok=True)

    _run(["model_converter",
          "--input_path", str(sparse_dir / "0"),
          "--output_path", str(output_txt_dir),
          "--output_type", "TXT"])

    logger.info(f"COLMAP reconstruction done → {sparse_dir}")
    return sparse_dir


def _run(args: list[str]) -> None:
    cmd = [COLMAP_PATH] + args
    logger.info(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        raise RuntimeError(f"COLMAP not found at '{COLMAP_PATH}'. Please check configuration.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"COLMAP step failed: {e}")