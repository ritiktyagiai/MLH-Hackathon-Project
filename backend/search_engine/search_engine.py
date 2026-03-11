import os
from typing import List, Dict
from google import genai

def search_timeline(query: str, timeline: List[Dict[str, str]]) -> str:
    """
    Uses Gemini to answer natural language questions about the timeline
    and return relevant timestamps and descriptions.
    """
    if not timeline:
        return "No events in timeline to search."
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "API Key is missing."
        
    client = genai.Client(api_key=api_key)
    
    input_text = ""
    for e in timeline:
        input_text += f"[{e['timestamp']}] {e['description']}\n"
        
    prompt = (
        "You are an AI assistant helping a user query a CCTV video timeline.\n"
        "Based ONLY on the provided timeline, answer the user's question.\n"
        "Include the relevant timestamps in your answer.\n"
        "If the answer is not in the timeline, say 'I could not find any events matching your query in the timeline.'\n\n"
        f"Timeline:\n{input_text}\n\n"
        f"User Query: {query}\n"
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error searching timeline: {e}")
        return "Search failed due to an API error."
