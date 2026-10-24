import os
import streamlit as st
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

st.set_page_config(page_title="स्मार्ट वीडियो मेकर", page_icon="🎬")

st.title("🎬 ऑटोमैटिक वीडियो असेंबलर ऐप")
st.write("अपनी वॉइस (ऑडियो) और तस्वीरें अपलोड करें, ऐप खुद-ब-खुद उन्हें मिलाकर वीडियो बना देगा!")

# फोल्डर बनाएं
os.makedirs("temp", exist_ok=True)

# 1. ऑडियो फाइल अपलोड करें
audio_file = st.file_uploader("अपनी वॉइस (ऑडियो) फाइल चुनें", type=["mp3", "wav", "m4a"])

# 2. तस्वीरें अपलोड करें
image_files = st.file_uploader("तस्वीरें चुनें (एक या अधिक)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if st.button("वीडियो बनाएं"):
    if audio_file is not None and image_files:
        with st.spinner("वीडियो तैयार हो रहा है, कृपया थोड़ा इंतज़ार करें..."):
            
            # ऑडियो सेव करें
            audio_path = os.path.join("temp", audio_file.name)
            with open(audio_path, "wb") as f:
                f.write(audio_file.getbuffer())
            
            # तस्वीरें सेव करें
            image_paths = []
            for img in image_files:
                img_path = os.path.join("temp", img.name)
                with open(img_path, "wb") as f:
                    f.write(img.getbuffer())
                image_paths.append(img_path)
            
            # तस्वीरों को सॉर्ट करें (नाम या क्रम के हिसाब से)
            image_paths.sort()
            
            # MoviePy से वीडियो प्रोसेसिंग
            audio_clip = AudioFileClip(audio_path)
            total_duration = audio_clip.duration
            duration_per_image = total_duration / len(image_paths)
            
            clips = []
            for img_p in image_paths:
                clip = ImageClip(img_p).set_duration(duration_per_image)
                clips.append(clip)
                
            final_video = concatenate_videoclips(clips, method="compose")
            final_video = final_video.set_audio(audio_clip)
            
            output_path = os.path.join("temp", "final_output.mp4")
            final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
            
            st.success("सफलतापूर्वक वीडियो बन गया!")
            
            # वीडियो दिखाएं
            st.video(output_path)
            
            # डाउनलोड बटन दें
            with open(output_path, "rb") as file:
                st.download_button(
                    label="फाइनल वीडियो डाउनलोड करें",
                    data=file,
                    file_name="final_video.mp4",
                    mime="video/mp4"
                )
    else:
        st.error("कृपया अपनी वॉइस फाइल और कम से कम एक तस्वीर दोनों अपलोड करें!")

