import os
import cv2
import numpy as np
import time
from typing import List, Dict, Any
from google import genai
from PIL import Image

def remove_duplicate_frames(frames: List[Dict[str, Any]], threshold: float = 5.0) -> List[Dict[str, Any]]:
    """
    Removes near-duplicate frames using Mean Squared Error (MSE) to reduce API calls.
    Lowered threshold to 5.0 to detect subtle movements.
    """
    if not frames:
        return []
        
    filtered = [frames[0]]
    prev_img = cv2.imread(frames[0]["frame_path"])
    if prev_img is None:
        return frames # Fallback if error
        
    # Apply slight blur to remove camera noise before comparing
    prev_img = cv2.cvtColor(prev_img, cv2.COLOR_BGR2GRAY)
    prev_img = cv2.GaussianBlur(prev_img, (5, 5), 0)
    
    for f in frames[1:]:
        curr_img = cv2.imread(f["frame_path"])
        if curr_img is None:
            continue
            
        curr_img = cv2.cvtColor(curr_img, cv2.COLOR_BGR2GRAY)
        curr_img = cv2.GaussianBlur(curr_img, (5, 5), 0)
        
        # Calculate MSE
        err = np.sum((prev_img.astype("float") - curr_img.astype("float")) ** 2)
        err /= float(prev_img.shape[0] * prev_img.shape[1])
        
        if err > threshold:
            filtered.append(f)
            prev_img = curr_img
            
    return filtered

def analyze_frames(frames: List[Dict[str, Any]], batch_size: int = 5) -> List[Dict[str, str]]:
    """
    Analyzes frames using Gemini API in batches.
    Returns a list of analysis results with timestamps.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
        
    client = genai.Client(api_key=api_key)
    results = []
    
    # Pre-filter frames
    filtered_frames = remove_duplicate_frames(frames)
    
    # Process in batches
    for i in range(0, len(filtered_frames), batch_size):
        batch = filtered_frames[i:i + batch_size]
        
        prompt = (
            "You are a highly observant AI CCTV analysis system.\n"
            "I am providing a sequence of frames from a security camera.\n"
            "Carefully examine each frame for details. For each frame, detect and describe in detail:\n"
            "- People (count, clothing, actions)\n"
            "- Vehicles (make, color, movement)\n"
            "- Suspicious movement or loitering\n"
            "- Entry or exit events (doors, gates, screen edges)\n"
            "- Objects such as bags, packages, laptops, etc.\n"
            "\nEach frame provided is in chronological order, corresponding to the following timestamps:\n"
        )
        for idx, f in enumerate(batch):
            prompt += f"Image {idx+1} timestamp: {f['timestamp']}\n"
            
        prompt += (
            "\nProvide your analysis for each frame strictly in the following format:\n"
            "timestamp: [timestamp from list]\n"
            "description: [highly detailed description of ALL detected events, or 'No significant activity' if the frame is completely empty of action]\n"
            "\nRepeat this block for every single image provided."
        )
        
        contents = [prompt]
        
        for f in batch:
            try:
                img = Image.open(f["frame_path"])
                contents.append(img)
            except Exception as e:
                print(f"Error loading image {f['frame_path']}: {e}")
                
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents,
            )
            
            text = response.text
            
            # Simple parsing
            blocks = text.split("timestamp:")
            for block in blocks[1:]:
                lines = block.strip().split("\n")
                if len(lines) >= 1:
                    timestamp = lines[0].strip()
                    # The rest of the lines might contain the description
                    desc_text = "\n".join(lines[1:]).strip()
                    if desc_text.lower().startswith("description:"):
                        desc_text = desc_text[len("description:"):].strip()
                        
                    if desc_text and "no significant activity" not in desc_text.lower():
                        results.append({
                            "timestamp": timestamp,
                            "description": desc_text
                        })
                        
            # Simple rate limiting
            time.sleep(1) 
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            
    return results
