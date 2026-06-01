import argparse
from pathlib import Path
from src.pipeline.full_pipeline import run_full_pipeline
from src.pipeline.run_colmap import run_colmap
from src.viewer.viewer import visualize


def main():
    parser = argparse.ArgumentParser(description="Phone-to-3D: reconstruct a 3D point cloud from a video.")
    parser.add_argument("video", help="Path to input video file")
    parser.add_argument("--name", default="output", help="Name for this reconstruction run (default: output)")
    parser.add_argument("--view", action="store_true", help="Open 3D viewer after reconstruction")
    args = parser.parse_args()

    ply_path = run_full_pipeline(args.video, args.name)

    if args.view:
        visualize(ply_path)


#if __name__ == "__main__":
#    main()
if __name__ == "__main__":
    image_folder = Path("data/input_images/gerard_hall/images")
    colmap_output = Path("data/colmap/gerard_hall")
    run_colmap(image_folder, colmap_output)