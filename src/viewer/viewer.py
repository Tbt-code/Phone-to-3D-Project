from pathlib import Path
import open3d as o3d
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)


def load_point_cloud(ply_path: Path) -> o3d.geometry.PointCloud:
    if not ply_path.exists():
        raise FileNotFoundError(f"Point cloud not found: {ply_path}")
    pcd = o3d.io.read_point_cloud(str(ply_path))
    logger.info(f"Loaded {len(pcd.points)} points from {ply_path}")
    return pcd


def visualize(ply_path: Path) -> None:
    pcd = load_point_cloud(ply_path)
    o3d.visualization.draw_geometries(
        [pcd],
        window_name="Phone-to-3D Viewer",
        width=1280,
        height=720,
    )
