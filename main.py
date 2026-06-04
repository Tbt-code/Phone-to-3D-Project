import argparse
from pathlib import Path
from src.pipeline.full_pipeline import run_full_pipeline
from src.viewer.viewer import visualize


def main():
    parser = argparse.ArgumentParser(description="Phone-to-3D: Reconstruct a 3D model from a video or image sequence.")
    parser.add_argument("input_path", help="Path to input video file or image directory")
    parser.add_argument("--name", default="output", help="Name for this reconstruction run (default: output)")
    parser.add_argument("--video", action="store_true", help="Set this flag if the input path is a video file")
    parser.add_argument("--view", action="store_true", help="Open the 3D viewer after reconstruction completes")
    args = parser.parse_args()

    # Triggers the end-to-end full pipeline algorithmically
    ply_path = run_full_pipeline(args.input_path, args.name, is_video=args.video)

    if args.view:
        visualize(ply_path)


if __name__ == "__main__":
    # --- Option A: Standard Production Execution via Command Line Arguments ---
    # To run this via terminal: python main.py data/input_images/gerard_hall/images --name gerard_hall_run --view
    # main()

    # --- Option B: Direct Script Execution for Automated Testing (Gerard Hall Dataset) ---
    # This directly triggers the pipeline without requiring command line inputs during development
    dataset_folder = "data/input_images/gerard_hall/images"
    project_name = "gerard_hall"
    
    # Executing the full pipeline with is_video=False to skip video frame extraction 
    # and directly process the static benchmark image dataset through COLMAP and OpenMVS
    run_full_pipeline(input_path=dataset_folder, output_name=project_name, is_video=False)