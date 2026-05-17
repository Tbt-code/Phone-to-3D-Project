import subprocess
from pathlib import Path
from src.config import FRAME_RATE,FFMPEG_PATH

def extract_frames(video_path:str,output_dir:Path):
    output_dir.mkdir(parents=True,exist_ok=True)

    command = [FFMPEG_PATH,
        "-i",video_path,
        "-vf",f"fps={FRAME_RATE}",
        str(output_dir/"frame_%04d.jpg")
    ]

    print("Running FFmpeg...")
    subprocess.run(command,check=True)
    print("Frame extraction complete.")

