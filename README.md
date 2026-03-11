# AI CCTV Intelligence System

The AI CCTV Intelligence System analyzes long CCTV videos and automatically generates a structured timeline of events using OpenCV and the Gemini Vision API. It provides a FastAPI backend for processing and a Streamlit dashboard for a user-friendly interface.

## System Capabilities
- **Video Ingestion:** Upload CCTV footage (`.mp4`, `.mov`, `.avi`).
- **Video Processing:** Efficiently extracts frames using OpenCV.
- **AI Analysis:** Uses Gemini 2.5 Flash to analyze frames and detect people, vehicles, suspicious movements, and objects.
- **Timeline Engine:** Merges and dedupes events into a concise JSON timeline using Gemini NLP capabilities.
- **Search Engine:** Query the timeline using natural language.
- **Dashboard:** Interactive Streamlit UI for viewing progress, filters, and summaries.

## Environment Setup

### 1. Requirements
Ensure you have Python 3.9+ installed. It is recommended to use a virtual environment.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file in the root directory (or rename `.env.example`) and add your Gemini API Key:
```text
GEMINI_API_KEY=your_actual_api_key_here
```
Note: Ensure you have the `google-genai` SDK properly installed as per the requirements.

## Step-by-Step Run Guide

### Step 1: Start the Backend Server
Open a terminal in the root project folder (`AI_CCTV_Intelligence_System`):
```bash
uvicorn backend.api.api_server:app --reload
```
The FastAPI server will run on `http://localhost:8000`.

### Step 2: Start the Frontend App
Open a second terminal in the project folder:
```bash
streamlit run frontend/frontend_app.py
```
The Streamlit app will automatically open in your browser (usually `http://localhost:8501`).

### Step 3: Usage
1. Open the Streamlit Dashboard.
2. Upload a CCTV video file.
3. Click "Upload and Analyze".
4. Wait for the pipeline to finish processing (you will see the progress bar update).
5. View the final video summary, filter the event timeline, and use the natural language search bar!

## Project Structure
```text
AI_CCTV_Intelligence_System/
├── backend/
│   ├── api/
│   │   └── api_server.py
│   ├── ai_analysis/
│   │   └── gemini_analyzer.py
│   ├── search_engine/
│   │   └── search_engine.py
│   ├── timeline_engine/
│   │   └── timeline_builder.py
│   └── video_processing/
│       ├── frame_extractor.py
│       └── video_loader.py
├── frontend/
│   └── frontend_app.py
├── data/
│   ├── processed/
│   └── uploads/
├── .env.example
├── requirements.txt
└── README.md
```
