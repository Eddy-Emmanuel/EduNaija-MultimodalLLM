import os
import streamlit as st
from io import BytesIO
import wave
import numpy as np
from openai import OpenAI
from app.agents.multiagent import compiled_agent_graph
from audio_recorder_streamlit import audio_recorder
from app.configurations.accesskeys import accesskeys_config

st.title("EduNaija AI Tutor")
st.write("Type a question or record your question live.")

os.environ["OPENAI_API_KEY"] = accesskeys_config.OPENAI_API_KEY

input_type = st.radio("Choose input type:", ["Text", "Record Audio"])
user_input = None
client = OpenAI()

def make_wav_file(audio_bytes, sample_rate=44100):
    """Convert raw audio bytes from audio_recorder to a valid WAV file."""
    audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
    buf = BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(sample_rate)
        wf.writeframes(audio_array.tobytes())
    buf.seek(0)
    buf.name = "audio.wav"  # Add filename attribute
    return buf

# --- Text Input ---
if input_type == "Text":
    user_input = st.text_area("Type your question here:")

# --- Record Audio ---
elif input_type == "Record Audio":
    st.write("Click record and speak your question:")
    audio_bytes = audio_recorder()
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.write("Transcribing audio with Whisper...")
        
        try:
            wav_file = make_wav_file(audio_bytes)
            
            # Pass the file with proper context manager
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", wav_file, "audio/wav"),
                model="whisper-1"
            )
            
            # Access the text attribute correctly
            user_input = transcription.text
            st.write("Transcribed Text:", user_input)
            
        except Exception as e:
            st.error(f"Transcription error: {str(e)}")
            user_input = None

# --- Agent Response ---
if st.button("Get Response") and user_input:
    with st.spinner("Getting response..."):
        try:
            response = compiled_agent_graph.invoke({"query": user_input})
            st.write("Agent Response:")
            st.success(response["final_answer"])
        except Exception as e:
            st.error(f"Error getting response: {str(e)}")