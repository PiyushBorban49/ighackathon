import streamlit as st
import os
from processors.pdf_parser import extract_text_from_pdf
from processors.llm_engine import generate_script_and_code, generate_quiz
from processors.audio_engine import generate_audio
from processors.video_engine import render_manim_video, merge_audio_video

st.set_page_config(page_title="AI Tutor", layout="wide")

st.title("📚 AI Video Tutor & Quiz Generator")
st.markdown("Upload a PDF or enter a topic to generate a video lesson.")

# Sidebar for Input
with st.sidebar:
    input_mode = st.radio("Input Mode", ["Topic", "PDF"])
    
    user_text = ""
    if input_mode == "Topic":
        topic = st.text_input("Enter Topic (e.g., Photosynthesis)")
        if topic:
            user_text = topic
    else:
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_file:
            with st.spinner("Extracting text..."):
                user_text = extract_text_from_pdf(uploaded_file)
                st.success("PDF Loaded!")

    generate_btn = st.button("Generate Video Lesson")

# Main Content Area
if generate_btn and user_text:
    
    # 1. Processing State
    status = st.empty()
    progress = st.progress(0)
    
    try:
        # Step 1: AI Brain
        status.text("🧠 Analyzing content and writing script...")
        data = generate_script_and_code(user_text)
        
        if "error" in data:
            st.error(data["error"])
            st.stop()

        if not data:
            st.error("Failed to generate content. Try a simpler topic.")
            st.stop()
            
        script = data['narration']
        code = data['manim_code']
        progress.progress(25)
        
        # Step 2: Audio
        status.text("🗣️ Generating AI Voiceover...")
        generate_audio(script, "narration.mp3")
        progress.progress(50)
        
        # Step 3: Video Rendering (The hard part)
        status.text("🎬 Rendering Animation (This may take 1-2 mins)...")
        # Note: Manim output path depends on your OS and Manim version.
        # Usually: media/videos/scene/480p15/ExplanationScene.mp4
        raw_video_path = render_manim_video(code)
        
        if not raw_video_path:
            st.error("Animation failed even after self-repair. The code was too complex.")
            st.code(code, language='python') # Show user the code to debug
            st.stop()
            
        progress.progress(75)
        
        # Step 4: Merging
        status.text("✨ Finalizing Video...")
        final_video = merge_audio_video(raw_video_path, "narration.mp3")
        progress.progress(100)
        status.text("✅ Done!")
        
        # Display Results
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Video Lesson")
            st.video(final_video)
            
            with st.expander("View Script"):
                st.write(script)
        
        with col2:
            st.subheader("Interactive Quiz")
            if st.button("Generate Quiz for this Topic"):
                with st.spinner("Creating questions..."):
                    quiz_data = generate_quiz(script)
                    st.session_state['quiz'] = quiz_data
            
            if 'quiz' in st.session_state:
                for i, q in enumerate(st.session_state['quiz']):
                    st.write(f"**Q{i+1}: {q['question']}**")
                    choice = st.radio(f"Select answer for Q{i+1}", q['options'], key=f"q{i}")
                    if st.button(f"Check Answer {i+1}", key=f"btn{i}"):
                        if choice == q['answer']:
                            st.success("Correct!")
                        else:
                            st.error(f"Wrong. Correct: {q['answer']}")

    except Exception as e:
        st.error(f"An error occurred: {e}")