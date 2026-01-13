from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    return genai.Client(api_key=api_key)

def generate_script_and_code(topic_text):
    client = get_client()
    
    prompt = f"""
    You are an educational video generator.
    Topic: {topic_text[:2000]}
    
    Task:
    1. Write a short narration script (max 3 sentences).
    2. Write Python Manim code to visualize it.
    
    CRITICAL MANIM CODE CONSTRAINTS:
    - Class name MUST be 'ExplanationScene'.
    - STRICTLY FORBIDDEN: LaTeX, MathTex, Tex. You MUST use 'Text' class for all text.
    - STRICTLY FORBIDDEN: 3D scenes, complex graphs, external images.
    - Use ONLY simple shapes: Circle, Square, Rectangle, Line, Arrow.
    - Keep animations simple: FadeIn, Write, Create, Transform.
    - The code must be robust and "dumbed down" to ensure it renders without standard Manim installation errors.
    
    OUTPUT FORMAT:
    Return a raw JSON object with exactly these keys:
    {{
        "narration": "The text for the voiceover...",
        "manim_code": "from manim import *\\nclass ExplanationScene(Scene):..."
    }}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-preview-09-2025',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json" 
            )
        )
        
        data = json.loads(response.text)
        
        # Safety Check
        if "script" in data and "narration" not in data:
            data["narration"] = data["script"]
        
        if "code" in data and "manim_code" not in data:
            data["manim_code"] = data["code"]
            
        return data

    except Exception as e:
        return {"error": str(e)}

def attempt_code_fix(broken_code, error_message):
    client = get_client()
    prompt = f"""
    Fix this Manim code. It caused this error: {error_message}
    
    INSTRUCTIONS:
    - Simplify the code significantly.
    - REMOVE ALL LATEX (MathTex/Tex). Replace with 'Text' class.
    - Remove complex animations.
    
    Code: {broken_code}
    Return ONLY raw Python code.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-preview-09-2025',
            contents=prompt
        )
        return response.text.replace("```python", "").replace("```", "").strip()
    except:
        return broken_code

def generate_quiz(topic_text):
    client = get_client()
    prompt = f"""
    Generate 3 JSON multiple-choice questions about: {topic_text[:500]}
    Format: [{{"question": "...", "options": ["..."], "answer": "..."}}]
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-preview-09-2025',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except:
        return []