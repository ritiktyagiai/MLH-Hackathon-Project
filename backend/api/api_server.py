import os
import sys
import json
import logging
from threading import Thread
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

# Ensure we can import from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env')))

from backend.video_processing.video_loader import save_uploaded_video, get_video_path
from backend.video_processing.frame_extractor import extract_frames
from backend.ai_analysis.gemini_analyzer import analyze_frames
from backend.timeline_engine.timeline_builder import generate_concise_timeline, generate_video_summary
from backend.search_engine.search_engine import search_timeline

app = FastAPI(title="AI CCTV Intelligence System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for processing status
# Format: { video_id: {"status": "processing", "progress": 0, "message": "Extracting frames...", "result": None} }
processing_jobs: Dict[str, Dict[str, Any]] = {}

class SearchQuery(BaseModel):
    query: str

def process_video_pipeline(video_id: str, video_path: str):
    """
    Background worker that runs the full pipeline
    """
    try:
        # Step 1: Extract Frames
        processing_jobs[video_id]["message"] = "Extracting frames..."
        processing_jobs[video_id]["progress"] = 10
        frames = extract_frames(video_path, video_id, interval_seconds=2)
        
        # Step 2: AI Analysis
        processing_jobs[video_id]["message"] = "Analyzing frames with Gemini AI..."
        processing_jobs[video_id]["progress"] = 40
        raw_events = analyze_frames(frames, batch_size=5)
        
        # Step 3: Timeline generation
        processing_jobs[video_id]["message"] = "Generating concise timeline..."
        processing_jobs[video_id]["progress"] = 80
        concise_timeline = generate_concise_timeline(raw_events)
        
        # Step 4: Video Summary
        processing_jobs[video_id]["message"] = "Generating video summary..."
        processing_jobs[video_id]["progress"] = 90
        summary = generate_video_summary(concise_timeline)
        
        # Step 5: Save and Finish
        result = {
            "timeline": concise_timeline,
            "summary": summary,
            "raw_events": raw_events
        }
        
        # Save result to file for persistence
        result_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', video_id))
        os.makedirs(result_dir, exist_ok=True)
        with open(os.path.join(result_dir, 'result.json'), 'w') as f:
            json.dump(result, f)
            
        processing_jobs[video_id]["status"] = "completed"
        processing_jobs[video_id]["progress"] = 100
        processing_jobs[video_id]["message"] = "Processing complete."
        processing_jobs[video_id]["result"] = result
        
    except Exception as e:
        processing_jobs[video_id]["status"] = "error"
        processing_jobs[video_id]["message"] = str(e)


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    success, filepath, data = save_uploaded_video(file.filename, file.file)
    if not success:
        raise HTTPException(status_code=400, detail=data)
    
    return {"video_id": data, "message": "Upload successful"}


@app.post("/start_processing/{video_id}")
async def start_processing(video_id: str, background_tasks: BackgroundTasks):
    video_path = get_video_path(video_id)
    if not video_path:
        raise HTTPException(status_code=404, detail="Video not found")
        
    processing_jobs[video_id] = {
        "status": "processing",
        "progress": 0,
        "message": "Starting pipeline...",
        "result": None
    }
    
    background_tasks.add_task(process_video_pipeline, video_id, video_path)
    return {"message": "Processing started in background"}


@app.get("/status/{video_id}")
async def get_status(video_id: str):
    if video_id not in processing_jobs:
        # Check if it was processed before
        result_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', video_id, 'result.json'))
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                result = json.load(f)
            return {"status": "completed", "progress": 100, "message": "Loaded from cache", "result": result}
        raise HTTPException(status_code=404, detail="Job not found")
        
    job = processing_jobs[video_id]
    
    response = {
        "status": job["status"],
        "progress": job["progress"],
        "message": job["message"]
    }
    
    if job["status"] == "completed":
        response["result"] = job["result"]
        
    return response

@app.post("/search/{video_id}")
async def search_video(video_id: str, query: SearchQuery):
    result_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', video_id, 'result.json'))
    if not os.path.exists(result_file):
        raise HTTPException(status_code=404, detail="Results not found for this video")
        
    with open(result_file, 'r') as f:
        data = json.load(f)
        
    timeline = data.get("timeline", [])
    answer = search_timeline(query.query, timeline)
    return {"answer": answer}
