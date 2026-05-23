import subprocess
import os
from pathlib import Path
from src.config import COLMAP_PATH

def run_colmap(image_path,output_path):

    image_path = Path(image_path)
    output_path = Path(output_path)

    output_path.mkdir(parents=True, exist_ok=True)

    database_path = output_path / "database.db"
    sparse_path = output_path / "sparse"

    sparse_path.mkdir(exist_ok=True)

    print("Starting COLMAP pipeline...")
    print("Running feature extraction...")

    subprocess.run([
        COLMAP_PATH,
        "feature_extractor",
        "--database_path", str(database_path),
        "--image_path", str(image_path)
    ],check=True)

    print("Running feature matching...")
    subprocess.run([
        COLMAP_PATH,
        "exhaustive_matcher",
        "--database_path", str(database_path)
    ],check=True)

    print("Running sparse reconstruction...")
    subprocess.run([
        COLMAP_PATH,
        "mapper",
        "--database_path", str(database_path),
        "--image_path", str(image_path),
        "--output_path", str(sparse_path),
    ],check=True)

    print("COLMAP sparse reconstruction complete.")
