import os
import streamlit as st
from datetime import datetime
from app.agents.multiagent import agent
from app.agents.rag import set_pdf_path  # ← ADD THIS IMPORT
from app.configurations.accesskeys import accesskeys_config

# Page configuration
st.set_page_config(
    page_title="EduNaija AI Tutor",
    page_icon="📚",
    layout="wide"
)

st.title("📚 EduNaija AI Tutor")
st.write("Ask questions in Yoruba, Hausa, Igbo, or English.")

# Set API key
os.environ["OPENAI_API_KEY"] = accesskeys_config.OPENAI_API_KEY

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "temp_path" not in st.session_state:
    st.session_state.temp_path = None

# Language configuration
LANGUAGES = {
    "English": "en",
    "Yoruba": "yo",
    "Hausa": "ha",
    "Igbo": "ig"
}

# UI Text translations
TRANSLATIONS = {
    "placeholder": {
        "en": "Type your question here...",
        "yo": "Kọ ìbéèrè rẹ síbí...",
        "ha": "Rubuta tambayarka a nan...",
        "ig": "Dee ajụjụ gị ebe a..."
    },
    "button": {
        "en": "Get Response",
        "yo": "Gba Ìdáhùn",
        "ha": "Sami Amsa",
        "ig": "Nweta Nzaghachi"
    },
    "response_label": {
        "en": "Agent Response:",
        "yo": "Ìdáhùn Agenti:",
        "ha": "Amsar Wakili:",
        "ig": "Nzaghachi Onye Nnọchiteanya:"
    },
    "no_answer": {
        "en": "No answer returned",
        "yo": "Kò sí ìdáhùn tí ó padà",
        "ha": "Babu amsar da aka dawo",
        "ig": "Enweghị nzaghachi alọghachiri"
    },
    "error": {
        "en": "Error getting response",
        "yo": "Àṣìṣe nínú gbígba ìdáhùn",
        "ha": "Kuskure wajen samun amsa",
        "ig": "Njehie n'inweta nzaghachi"
    },
    "upload_success": {
        "en": "PDF uploaded successfully!",
        "yo": "PDF ti gba àṣeyọrí!",
        "ha": "An loda PDF cikin nasara!",
        "ig": "Ebulitere PDF nke ọma!"
    },
    "clear_chat": {
        "en": "Clear Chat History",
        "yo": "Pa Ìtàn Ìfọ̀rọ̀wérọ̀ Rẹ́",
        "ha": "Share Tarihin Hira",
        "ig": "Hichapụ Akụkọ Mkparịta Ụka"
    }
}

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    selected_language = st.selectbox(
        "Select your language / Yan zaɓin harshenku / Yan họrọ asụsụ gị / Yan fẹ́ èdè rẹ:",
        list(LANGUAGES.keys())
    )
    
    language_code = LANGUAGES[selected_language]
    
    st.divider()
    
    # PDF Upload
    st.subheader("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Upload a PDF for context-based questions", 
        type="pdf",
        help="Upload educational materials for RAG-based questioning"
    )
    
    if uploaded_file:
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.temp_path = temp_path
        set_pdf_path(temp_path)  # ← ADD THIS LINE - This fixes the error!
        st.success(TRANSLATIONS["upload_success"].get(language_code, "PDF uploaded successfully!"))
    
    st.divider()
    
    # Clear chat button
    if st.button(TRANSLATIONS["clear_chat"].get(language_code, "Clear Chat History")):
        st.session_state.messages = []
        st.rerun()
    
    # Display chat count
    st.caption(f"Messages: {len(st.session_state.messages)}")

# Main chat interface
st.subheader("💬 Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input(
    TRANSLATIONS["placeholder"].get(language_code, "Type your question here...")
)

# Process user input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Add language and timestamp context to the query
            query_with_context = (
                f"[Your Name: EduNaija AI Tutor] "
                f"[Your Creator: Eddy and Israel Odeajo]"
                f"[Selected Response Language: {selected_language}] "
                f"[Current time: {datetime.now().isoformat()}] "
                f"{user_input}"
            )
            
            # Add PDF context if available
            if st.session_state.temp_path:
                query_with_context = f"[PDF Document Available] {query_with_context}"
            
            # Stream the response
            for chunk in agent.stream(
                {
                    "messages": [
                        ("user", query_with_context)
                    ]
                },
                stream_mode="messages",
            ):
                # Extract content from stream chunks
                if isinstance(chunk, tuple) and len(chunk) >= 1:
                    msg_chunk = chunk[0]
                    
                    if hasattr(msg_chunk, 'content') and msg_chunk.content:
                        full_response += msg_chunk.content
                        # Update display with streaming cursor
                        response_placeholder.markdown(full_response + "▌")
            
            # Final response
            if full_response:
                response_placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
            else:
                no_answer_msg = TRANSLATIONS["no_answer"].get(
                    language_code, 
                    "No answer returned"
                )
                response_placeholder.warning(no_answer_msg)
                
        except Exception as e:
            error_prefix = TRANSLATIONS["error"].get(language_code, "Error getting response")
            error_message = f"{error_prefix}: {str(e)}"
            response_placeholder.error(error_message)
            st.session_state.messages.append(
                {"role": "assistant", "content": f"⚠️ {error_message}"}
            )

# Footer
st.divider()
st.caption("🇳🇬 EduNaija AI Tutor - Empowering education across Nigeria")