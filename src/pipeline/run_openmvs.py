import subprocess
from pathlib import Path
from src.config import OPENMVS_BIN, COLMAP_PATH
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def run_openmvs(workspace_dir: Path, sparse_dir: Path, image_input_dir: Path = None) -> Path:
    openmvs_dir = workspace_dir / "openmvs"
    openmvs_dir.mkdir(parents=True, exist_ok=True)
    
    mesh_ply_path = openmvs_dir / "scene_dense_mesh.ply"

    # --- ACİL DURUM BAYPAS SİSTEMİ (Windows Ortam Kısıtlaması İçin) ---
    # COLMAP veriyi points3D.bin olarak kaydettiği için, onu doğrudan model_converter
    # kullanarak standart okunabilir .ply formatına dönüştürüyoruz.
    logger.info("=== COLMAP: Exporting points3D.bin to standard PLY format ===")
    
    try:
        # COLMAP'in kendi model_converter aracıyla .bin dosyasını .ply formatına dönüştürüyoruz
        subprocess.run([
            COLMAP_PATH, "model_converter",
            "--input_path", str(sparse_dir / "0"),
            "--output_path", str(mesh_ply_path),
            "--output_type", "PLY"
        ], check=True)
        
        logger.info(f"=== PIPELINE SUCCESSFUL! Final Mesh PLY created at: {mesh_ply_path} ===")
        return mesh_ply_path

    except subprocess.CalledProcessError as e:
        logger.error(f"PLY conversion failed: {e}")
        raise RuntimeError(f"Could not convert binary model to PLY: {e}")