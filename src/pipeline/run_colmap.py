import subprocess
from pathlib import Path
from src.config import COLMAP_PATH
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)


def run_colmap(image_dir: Path, workspace_dir: Path) -> Path:
    database = workspace_dir / "database.db"
    sparse_dir = workspace_dir / "sparse"
    sparse_dir.mkdir(parents=True, exist_ok=True)

    _run(["feature_extractor",
          "--database_path", str(database),
          "--image_path", str(image_dir),
          "--ImageReader.single_camera", "1",
          "--SiftExtraction.max_num_features", "8192"])

    #_run(["exhaustive_matcher",
    #      "--database_path", str(database),
    #      "--SiftMatching.min_num_inliers", "15"])

    _run([
    "exhaustive_matcher",
    "--database_path", str(database)
    ])
    
    _run(["mapper",
          "--database_path", str(database),
          "--image_path", str(image_dir),
          "--output_path", str(sparse_dir),
          "--Mapper.init_min_num_inliers", "15",
          "--Mapper.abs_pose_min_num_inliers", "15",
          "--Mapper.min_num_matches", "10"])

    _run(["model_converter",
          "--input_path", str(sparse_dir / "0"),
          "--output_path", str(sparse_dir / "0"),
          "--output_type", "TXT"])

    logger.info(f"COLMAP reconstruction done → {sparse_dir}")
    return sparse_dir


def _run(args: list[str]) -> None:
    cmd = [COLMAP_PATH] + args
    logger.info(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        raise RuntimeError(f"COLMAP not found at '{COLMAP_PATH}'. Install with: brew install colmap")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"COLMAP step failed: {e}")
