import streamlit as st
import requests
import time
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI CCTV Intelligence System", layout="wide")

st.title("📹 AI CCTV Intelligence System")
st.markdown("Automated surveillance analysis using Gemini Vision API")

if "video_id" not in st.session_state:
    st.session_state.video_id = None
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False
if "result" not in st.session_state:
    st.session_state.result = None

# Video Upload Section
st.header("1. Upload CCTV Footage")
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None and not st.session_state.video_id:
    if st.button("Upload and Analyze"):
        with st.spinner("Uploading video..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "video/mp4")}
            try:
                # Upload
                upload_res = requests.post(f"{API_URL}/upload", files=files)
                if upload_res.status_code == 200:
                    video_id = upload_res.json()["video_id"]
                    st.session_state.video_id = video_id
                    
                    # Start processing
                    process_res = requests.post(f"{API_URL}/start_processing/{video_id}")
                    if process_res.status_code == 200:
                        st.success("Upload successful! Starting analysis...")
                        st.rerun()
                    else:
                        st.error(f"Failed to start processing: {process_res.text}")
                else:
                    st.error(f"Upload failed: {upload_res.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

# Processing Progress Section
if st.session_state.video_id and not st.session_state.processing_complete:
    st.header("2. Processing Status")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Polling loop
    poll_count = 0
    poll_placeholder = st.empty()
    while True:
        try:
            res = requests.get(f"{API_URL}/status/{st.session_state.video_id}")
            if res.status_code == 200:
                data = res.json()
                progress = data.get("progress", 0)
                status = data.get("status", "")
                message = data.get("message", "")
                
                progress_bar.progress(progress / 100.0)
                status_text.text(f"Status: {status.capitalize()} - {message}")
                
                if status == "completed":
                    st.session_state.processing_complete = True
                    st.session_state.result = data.get("result")
                    st.rerun()
                    break
                elif status == "error":
                    st.error(f"Processing error: {message}")
                    break
                    
            time.sleep(2)
            poll_count += 1
            if poll_count % 5 == 0:
                poll_placeholder.text(f"Still polling... {poll_count} attempts")
        except Exception as e:
            st.error("Error communicating with API")
            break

# Results Section
if st.session_state.processing_complete and st.session_state.result:
    st.header("3. Analysis Results")
    result = st.session_state.result
    
    # Summary
    st.subheader("Video Summary")
    st.info(result.get("summary", "No summary available."))
    
    st.divider()
    
    # Layout for Timeline and Search
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Event Timeline")
        timeline = result.get("timeline", [])
        
        # Filtering
        filter_options = ["All", "People", "Vehicles", "Suspicious", "Entry/Exit", "Objects"]
        selected_filter = st.selectbox("Filter Events", filter_options)
        
        filtered_timeline = []
        for event in timeline:
            desc = event["description"].lower()
            if selected_filter == "All":
                filtered_timeline.append(event)
            elif selected_filter == "People" and any(w in desc for w in ["person", "people", "individual", "man", "woman"]):
                filtered_timeline.append(event)
            elif selected_filter == "Vehicles" and any(w in desc for w in ["car", "vehicle", "truck", "van", "sedan"]):
                filtered_timeline.append(event)
            elif selected_filter == "Suspicious" and any(w in desc for w in ["suspicious", "running", "stealing", "loitering"]):
                filtered_timeline.append(event)
            elif selected_filter == "Entry/Exit" and any(w in desc for w in ["enter", "exit", "leave", "arrive"]):
                filtered_timeline.append(event)
            elif selected_filter == "Objects" and any(w in desc for w in ["bag", "package", "box", "item"]):
                filtered_timeline.append(event)
                
        if filtered_timeline:
            df = pd.DataFrame(filtered_timeline)
            st.table(df)
        else:
            st.write("No events match the selected filter.")
            
    with col2:
        st.subheader("Natural Language Search")
        st.write("Ask questions about the footage!")
        
        with st.form("search_form"):
            query = st.text_input("e.g., 'When did the red car appear?'")
            submit_button = st.form_submit_button("Search")
            
        if submit_button:
            if query:
                with st.spinner("Searching..."):
                    try:
                        search_res = requests.post(
                            f"{API_URL}/search/{st.session_state.video_id}",
                            json={"query": query}
                        )
                        if search_res.status_code == 200:
                            answer = search_res.json().get("answer", "No answer found.")
                            st.success(answer)
                        else:
                            st.error("Search failed.")
                    except Exception as e:
                        st.error(f"Search API error: {e}")
            else:
                st.warning("Please enter a query.")
                
    st.divider()
    if st.button("Analyze Another Video"):
        st.session_state.video_id = None
        st.session_state.processing_complete = False
        st.session_state.result = None
        st.rerun()
