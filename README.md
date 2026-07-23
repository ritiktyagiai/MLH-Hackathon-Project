# 🚨 AI CCTV Intelligence System

An **AI-powered surveillance analysis platform** that transforms long CCTV footage into a **structured, searchable timeline of events**.
Instead of manually reviewing **hours of video**, investigators receive **AI-generated insights, summaries, and event detection** in minutes.

Built using **OpenCV, Gemini Vision API, FastAPI, and Streamlit**.


# 📌 The Problem

Modern cities generate **massive amounts of CCTV footage** every day.

Investigators and security teams often face challenges such as:

* ⏱ **Manually watching 6–10 hours of footage**
* 🔎 Difficulty identifying **critical moments in long recordings**
* 🚗 Trouble determining **accident causes**
* 🕵️ Slow investigation due to **lack of structured evidence**
* 📂 No easy way to **search events inside videos**

For example:

> After a road accident, police may need to review **8+ hours of CCTV footage** just to find the exact moment and cause.

This process is **time-consuming, inefficient, and prone to human error.**



# 💡 The Solution

The **AI CCTV Intelligence System** automatically analyzes CCTV footage and converts it into a **timeline of meaningful events** using AI.

Instead of watching hours of footage, users can:

* View a **timeline of detected events**
* Search events using **natural language**
* Quickly understand **what happened and when**

It acts like an **AI investigator for surveillance footage**.



# 🚓 How It Helps Investigations

This system can significantly assist **law enforcement, security teams, and investigators**.

### Accident Investigation

* Detect **vehicles, people, and unusual movements**
* Identify the **exact moment an accident occurred**
* Provide **visual evidence timeline**

### Crime Investigation

* Detect suspicious activity
* Track **movement patterns**
* Quickly find **important moments**

### Time Efficiency

Instead of watching **8 hours of video**, investigators can review:

```
AI Generated Timeline
---------------------
08:12 AM — White car enters parking area
08:14 AM — Two individuals exit vehicle
08:16 AM — Suspicious movement near gate
08:18 AM — Motorcycle collision detected
```

This reduces investigation time from **hours → minutes**.



# ✨ Key Features

### 📥 Video Ingestion

Upload CCTV footage in formats such as:

* `.mp4`
* `.mov`
* `.avi`


### 🎞 Video Frame Processing

Using **OpenCV**, the system extracts frames efficiently for analysis.



### 🧠 AI Vision Analysis

Powered by **Gemini 2.5 Flash Vision**, the system detects:

* 👤 People
* 🚗 Vehicles
* 📦 Objects
* ⚠ Suspicious movements
* 🚨 Possible incidents



### 🕒 Smart Timeline Generation

AI merges detections and creates a **clean chronological event timeline**.

Example output:

```json
[
  {
    "time": "00:02:13",
    "event": "Person enters parking lot"
  },
  {
    "time": "00:04:55",
    "event": "Two vehicles collide"
  }
]
```


### 🔎 Natural Language Search

Users can search events like:

```
"Show when the accident happened"
"Find when a car entered"
"Suspicious activity near the gate"
```

The system instantly finds relevant moments.



### 📊 Interactive Dashboard

A **Streamlit UI dashboard** allows users to:

* Upload videos
* Track processing progress
* View summaries
* Filter events
* Search the timeline


# ⚙️ System Architecture

```
CCTV Video
     │
     ▼
Frame Extraction (OpenCV)
     │
     ▼
AI Vision Analysis (Gemini)
     │
     ▼
Event Detection
     │
     ▼
Timeline Builder
     │
     ▼
Search Engine + Dashboard
```


# 🛠 Tech Stack

| Technology               | Purpose              |
| ------------------------ | -------------------- |
| **Python**               | Core development     |
| **OpenCV**               | Frame extraction     |
| **Gemini Vision API**    | AI video analysis    |
| **FastAPI**              | Backend API          |
| **Streamlit**            | Interactive frontend |
| **JSON Timeline Engine** | Event structuring    |



# 📂 Project Structure

```
AI_CCTV_Intelligence_System/
│
├── backend/
│   ├── api/
│   │   └── api_server.py
│   │
│   ├── ai_analysis/
│   │   └── gemini_analyzer.py
│   │
│   ├── search_engine/
│   │   └── search_engine.py
│   │
│   ├── timeline_engine/
│   │   └── timeline_builder.py
│   │
│   └── video_processing/
│       ├── frame_extractor.py
│       └── video_loader.py
│
├── frontend/
│   └── frontend_app.py
│
├── data/
│   ├── processed/
│   └── uploads/
│
├── .env.example
├── requirements.txt
└── README.md
```



# ⚡ Environment Setup

### 1️⃣ Requirements

Make sure you have:

```
Python 3.9+
pip
virtualenv (recommended)
```


### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```


### 3️⃣ Setup Environment Variables

Create a `.env` file in the root directory.

```
GEMINI_API_KEY="your_actual_api_key_here"
```



# ▶️ Step-by-Step Run Guide

## Step 1 — Start Backend Server

```bash
uvicorn backend.api.api_server:app --reload
```

Server will run at:

```
http://localhost:8000
```



## Step 2 — Start Frontend Dashboard

Open another terminal:

```bash
streamlit run frontend/frontend_app.py
```

Streamlit will open at:

```
http://localhost:8501
```


## Step 3 — Use the System

1️⃣ Open the **Streamlit Dashboard**

2️⃣ Upload a CCTV video

3️⃣ Click **Upload and Analyze**

4️⃣ Wait for AI processing

5️⃣ View:

* 📊 Video summary
* 🕒 Event timeline
* 🔎 Search results



# 🌍 Real-World Applications

This system can be used in:

* 🚓 **Police investigation**
* 🏙 **Smart city surveillance**
* 🏢 **Corporate security monitoring**
* 🚦 **Traffic accident analysis**
* 🛑 **Crime detection**



# 🚀 Future Improvements

Possible next upgrades:

* Real-time CCTV monitoring
* Vehicle number plate recognition
* Face recognition integration
* Multi-camera tracking
* Crime detection alerts
* AI-generated incident reports


# 🧠 Inspiration

Security teams shouldn’t waste hours watching silent video footage.

This project aims to transform CCTV systems from **passive recorders** into **intelligent investigative tools**.


# ⭐ If You Like This Project

Give it a ⭐ on GitHub and help make **AI-powered surveillance analysis smarter**.



