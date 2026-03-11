import cv2
import os
from typing import List, Dict, Any

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed')
os.makedirs(PROCESSED_DIR, exist_ok=True)

def extract_frames(video_path: str, video_id: str, interval_seconds: int = 2) -> List[Dict[str, Any]]:
    """
    Extracts frames from a video every `interval_seconds`.
    Returns a list of dictionaries containing frame paths and their timestamps.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    output_dir = os.path.abspath(os.path.join(PROCESSED_DIR, video_id, 'frames'))
    os.makedirs(output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Failed to open video: {video_path}")
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 30.0  # Fallback if fps cannot be determined
        
    frame_interval = int(round(fps * interval_seconds))
    
    extracted_frames = []
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            timestamp_sec = frame_count / fps
            
            # Format timestamp as HH:MM:SS
            hours = int(timestamp_sec // 3600)
            minutes = int((timestamp_sec % 3600) // 60)
            seconds = int(timestamp_sec % 60)
            timestamp_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            frame_filename = f"frame_{saved_count:05d}.jpg"
            frame_path = os.path.join(output_dir, frame_filename)
            
            # Save frame to disk
            cv2.imwrite(frame_path, frame)
            
            extracted_frames.append({
                "timestamp": timestamp_str,
                "timestamp_sec": timestamp_sec,
                "frame_path": frame_path
            })
            saved_count += 1
            
        frame_count += 1
        
    cap.release()
    return extracted_frames
