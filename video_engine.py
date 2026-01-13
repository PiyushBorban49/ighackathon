import subprocess
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from processors.llm_engine import attempt_code_fix

def render_manim_video(manim_code, scene_name="ExplanationScene", output_name="media/videos/scene/480p15/ExplanationScene.mp4"):
    """
    Writes code to file, runs Manim, and handles errors via LLM self-repair.
    """
    
    script_name = "scene.py"
    max_retries = 2
    
    for attempt in range(max_retries + 1):
        # 1. Write Code to File
        with open(script_name, "w") as f:
            f.write("from manim import *\n")
            # Ensure imports aren't duplicated
            if "from manim import *" not in manim_code:
                f.write(manim_code)
            else:
                f.write(manim_code.replace("from manim import *", ""))

        # 2. Run Manim (Low quality -ql for speed, overwrite -y)
        # Capture stderr to catch errors
        result = subprocess.run(
            ["manim", "-ql", script_name, scene_name], 
            capture_output=True, 
            text=True
        )

        # 3. Check for success
        if result.returncode == 0 and os.path.exists(output_name):
            return output_name
        
        # 4. Handle Failure
        print(f"Attempt {attempt+1} failed. Error: {result.stderr[-500:]}") # Print last 500 chars of error
        
        if attempt < max_retries:
            print("Attempting Self-Repair...")
            manim_code = attempt_code_fix(manim_code, result.stderr[-1000:])
        else:
            print("All repair attempts failed.")
            return None

def merge_audio_video(video_path, audio_path, output_path="final_video.mp4"):
    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        # Manim video might be shorter/longer than audio.
        # Strategy: Freeze the last frame of video if audio is longer.
        if audio.duration > video.duration:
            # Loop the last frame to fill time? 
            # Easier: Just speed up/slow down or loop. 
            # For simplicity: Set video duration to match audio (this might speed up video)
            # Better approach for lectures: Extend the last frame.
            video = video.set_duration(audio.duration) 
        else:
            video = video.subclip(0, audio.duration)
            
        final = video.set_audio(audio)
        final.write_videofile(output_path, codec="libx264", audio_codec="aac")
        return output_path
    except Exception as e:
        print(f"Merging Error: {e}")
        return None