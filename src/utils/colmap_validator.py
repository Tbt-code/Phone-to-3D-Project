import os
from pathlib import Path
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def sanitize_colmap_text_files(sparse_txt_dir: Path, image_dir: Path):
    """
    Sanitizes COLMAP text files to prevent OpenMVS InterfaceCOLMAP crashes.
    Specifically:
    1. Ensures images.txt uses ONLY the image filename (not absolute paths).
    2. Validates that every image listed actually exists in the image_dir.
    3. Forces Unix-style line endings to avoid C++ parser issues on Windows.
    """
    images_file = sparse_txt_dir / "images.txt"
    if not images_file.exists():
        raise FileNotFoundError(f"COLMAP images.txt not found at {images_file}")

    sanitized_lines = []
    with open(images_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    logger.info(f"Sanitizing {len(lines)} lines in images.txt...")

    line_idx = 0
    while line_idx < len(lines):
        line = lines[line_idx].strip()
        
        # Header or empty lines
        if not line or line.startswith("#"):
            sanitized_lines.append(line + "\n")
            line_idx += 1
            continue

        # Image registration lines in COLMAP format are every 2nd line:
        # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
        parts = line.split()
        if len(parts) >= 10:
            original_name = parts[9]
            # Force name to be just the filename to prevent OpenMVS recursion loops
            file_name = os.path.basename(original_name)
            
            if not (image_dir / file_name).exists():
                logger.warning(f"Image referenced in COLMAP not found in image folder: {file_name}")
            
            parts[9] = file_name
            sanitized_lines.append(" ".join(parts) + "\n")
            
            # The next line is the list of 2D points (skip it)
            if line_idx + 1 < len(lines):
                sanitized_lines.append(lines[line_idx + 1].strip() + "\n")
                line_idx += 1
        
        line_idx += 1

    with open(images_file, "w", newline="\n", encoding="utf-8") as f:
        f.writelines(sanitized_lines)
    
    logger.info("images.txt sanitized successfully.")