"""
Extracts frames from a directory of videos (e.g. FaceForensics++ .mp4 files)
into an output image folder, sampling every N frames to avoid near-duplicates.

Usage:
    python ml/dataset/extract_frames.py --input_dir <videos_dir> --output_dir <images_dir> --every_n_frames 15
"""
import argparse
import os

import cv2


def extract_frames(input_dir: str, output_dir: str, every_n_frames: int):
    os.makedirs(output_dir, exist_ok=True)
    video_files = [f for f in os.listdir(input_dir) if f.lower().endswith((".mp4", ".avi", ".mov"))]

    if not video_files:
        print(f"No video files found in {input_dir}")
        return

    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        cap = cv2.VideoCapture(video_path)
        video_name = os.path.splitext(video_file)[0]

        frame_idx, saved_idx = 0, 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % every_n_frames == 0:
                out_path = os.path.join(output_dir, f"{video_name}_frame{saved_idx:04d}.jpg")
                cv2.imwrite(out_path, frame)
                saved_idx += 1
            frame_idx += 1
        cap.release()
        print(f"{video_file}: saved {saved_idx} frames")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--every_n_frames", type=int, default=15)
    args = parser.parse_args()
    extract_frames(args.input_dir, args.output_dir, args.every_n_frames)
