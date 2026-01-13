import edge_tts
import asyncio

async def _generate_audio_async(text, output_file):
    # Voices: 'en-US-ChristopherNeural' (Male), 'en-US-AriaNeural' (Female)
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save(output_file)

def generate_audio(text, output_file="narration.mp3"):
    try:
        asyncio.run(_generate_audio_async(text, output_file))
        return True
    except Exception as e:
        print(f"Audio Error: {e}")
        return False