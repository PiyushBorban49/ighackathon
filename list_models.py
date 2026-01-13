import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def list_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("API Key not found")
        return

    client = genai.Client(api_key=api_key)
    try:
        # Pager object is not directly iterable in some versions, need to check how to list
        # Usually it's client.models.list()
        for m in client.models.list():
            if "gemini" in m.name:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
