from pathlib import Path
from src.pipeline.video_to_frames import extract_frames

if __name__ == "__main__":
    extract_frames("data/input_video/test.mp4",               
    Path("data/frames/test"))