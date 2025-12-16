import os
import streamlit as st
from app.agents.multiagent import agent
from app.configurations.accesskeys import accesskeys_config

st.title("EduNaija AI Tutor")
st.write("Type a question in Yoruba, Hausa, Igbo, or English.")

# Set API key
os.environ["OPENAI_API_KEY"] = accesskeys_config.OPENAI_API_KEY

# Language selection
LANGUAGES = {
    "English": "en",
    "Yoruba": "yo",
    "Hausa": "ha",
    "Igbo": "ig"
}

selected_language = st.selectbox(
    "Select your language / Yan zaɓin harshenku / Yan họrọ asụsụ gị / Yan fẹ́ èdè rẹ:",
    list(LANGUAGES.keys())
)

language_code = LANGUAGES[selected_language]

# Text Input
placeholder_text = {
    "en": "Type your question here...",
    "yo": "Kọ ìbéèrè rẹ síbí...",
    "ha": "Rubuta tambayarka a nan...",
    "ig": "Dee ajụjụ gị ebe a..."
}
user_input = st.text_area(placeholder_text.get(language_code, "Type your question here:"))

# --- Agent Response ---
button_labels = {
    "en": "Get Response",
    "yo": "Gba Ìdáhùn",
    "ha": "Sami Amsa",
    "ig": "Nweta Nzaghachi"
}

if st.button(button_labels.get(language_code, "Get Response")) and user_input:
    response_labels = {
        "en": "Agent Response:",
        "yo": "Ìdáhùn Agenti:",
        "ha": "Amsar Wakili:",
        "ig": "Nzaghachi Onye Nnọchiteanya:"
    }
    st.write(response_labels.get(language_code, "Agent Response:"))
    
    # Create placeholder for streaming response
    response_placeholder = st.empty()
    full_response = ""
    
    try:
        # Add language context to the query
        query_with_language = f"[Language: {selected_language}] {user_input}"
        
        # Use stream_mode="messages" for token-by-token streaming
        for chunk in agent.stream(
            {
                "messages": [
                    ("user", query_with_language)
                ]
            },
            stream_mode="messages",
        ):
            # Each chunk is a tuple: (AIMessageChunk, metadata)
            if isinstance(chunk, tuple) and len(chunk) >= 1:
                msg_chunk = chunk[0]
                
                # Extract content from AIMessageChunk
                if hasattr(msg_chunk, 'content') and msg_chunk.content:
                    full_response += msg_chunk.content
                    # Update display with cursor to show it's streaming
                    response_placeholder.markdown(full_response + "▌")
        
        # Final update with success styling
        if full_response:
            response_placeholder.success(full_response)
        else:
            no_answer_messages = {
                "en": "No answer returned",
                "yo": "Kò sí ìdáhùn tí ó padà",
                "ha": "Babu amsar da aka dawo",
                "ig": "Enweghị nzaghachi alọghachiri"
            }
            response_placeholder.warning(no_answer_messages.get(language_code, "No answer returned"))
            
    except Exception as e:
        error_messages = {
            "en": f"Error getting response: {str(e)}",
            "yo": f"Àṣìṣe nínú gbígba ìdáhùn: {str(e)}",
            "ha": f"Kuskure wajen samun amsa: {str(e)}",
            "ig": f"Njehie n'inweta nzaghachi: {str(e)}"
        }
        response_placeholder.error(error_messages.get(language_code, f"Error getting response: {str(e)}"))