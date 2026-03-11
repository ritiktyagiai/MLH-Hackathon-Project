import os
import json
from typing import List, Dict
from google import genai

def generate_concise_timeline(raw_events: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Takes raw frame analyses and uses Gemini to merge related events,
    remove duplicates, and produce a clean timeline.
    """
    if not raw_events:
        return []
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
        
    client = genai.Client(api_key=api_key)
    
    # Prepare the input text
    input_text = "Raw Events:\n"
    for e in raw_events:
        input_text += f"[{e['timestamp']}] {e['description']}\n"
        
    prompt = (
        "You are an expert security analyst. I will provide a list of raw events detected from a CCTV video.\n"
        "Your task is to create a concise, human-readable timeline.\n"
        "Instructions:\n"
        "1. Remove duplicate descriptions.\n"
        "2. Merge related events that happen continuously or in close succession into a single timeline entry.\n"
        "3. Keep descriptions professional and brief.\n"
        "4. Output MUST be valid JSON, consisting of a list of objects with 'timestamp' and 'description' keys.\n"
        "5. Do not wrap the JSON in Markdown formatting (no ```json ... ``` blocks). Return only the raw JSON array.\n\n"
        f"{input_text}"
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Parse JSON output
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        print("Model json output:", text)
        concise_timeline = json.loads(text.strip())
        return concise_timeline
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON timeline: {e}")
        return raw_events # fallback to raw
    except Exception as e:
        print(f"Error generating concise timeline: {e}")
        return raw_events # fallback to raw

def generate_video_summary(timeline: List[Dict[str, str]]) -> str:
    """
    Generates a high-level summary of the entire video based on the timeline.
    """
    if not timeline:
        return "No notable activity detected in the video."
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
        
    client = genai.Client(api_key=api_key)
    
    input_text = "Timeline:\n"
    for e in timeline:
        input_text += f"[{e['timestamp']}] {e['description']}\n"
        
    prompt = (
        "You are an expert security analyst. Based on the following event timeline from a CCTV video, "
        "write a high-level summary paragraph (2-4 sentences) that describes the overall activity.\n\n"
        f"{input_text}"
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating video summary: {e}")
        return "Summary generation failed."
