from pathlib import Path
from src.pipeline.video_to_frames import extract_frames
from src.pipeline.run_colmap import run_colmap


if __name__ == "__main__":
    extract_frames("data/input_video/test.mp4",               
    Path("data/frames/test"))

    frames_path = "data/frames/test"
    colmap_output = "data/colmap/test"

    run_colmap(frames_path,colmap_output)