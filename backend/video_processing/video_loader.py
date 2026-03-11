import os
import shutil
import uuid
from typing import Tuple

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

SUPPORTED_FORMATS = {'.mp4', '.mov', '.avi'}

def save_uploaded_video(filename: str, file_obj) -> Tuple[bool, str, str]:
    """
    Saves an uploaded video file to the uploads directory.
    Returns (success, filepath, message)
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        return False, "", f"Unsupported file format: {ext}. Supported formats are {', '.join(SUPPORTED_FORMATS)}"
    
    video_id = str(uuid.uuid4())
    new_filename = f"{video_id}{ext}"
    filepath = os.path.abspath(os.path.join(UPLOAD_DIR, new_filename))
    
    try:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file_obj, buffer)
        return True, filepath, video_id
    except Exception as e:
        return False, "", str(e)

def get_video_path(video_id: str) -> str:
    """Finds the video path given a video ID"""
    for file in os.listdir(UPLOAD_DIR):
        if file.startswith(video_id):
            return os.path.abspath(os.path.join(UPLOAD_DIR, file))
    return ""
