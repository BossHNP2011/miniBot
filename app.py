import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import tempfile
import os
from services.gemini_service import get_gemini_response
from components.chat_ui import render_chat_bubble, inject_css


try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  


st.set_page_config(
    page_title="MiniBot", 
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .css-1d391kg .css-17eq0hr {
        color: white;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: none;
    }
    
    /* Welcome section */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
        text-align: center;
        padding: 40px;
    }
    
    .bot-avatar {
        width: 80px;
        height: 80px;
        background: #00d4aa;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 35px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 212, 170, 0.3);
    }
    
    .welcome-title {
        font-size: 32px;
        font-weight: 700;
        color: white;
        margin-bottom: 15px;
    }
    
    .welcome-subtitle {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 40px;
    }
    
    /* Personas grid */
    .personas-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        max-width: 800px;
        width: 100%;
        margin-bottom: 30px;
    }
    
    .persona-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .persona-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 30px rgba(0, 212, 170, 0.2);
    }
    
    .persona-icon {
        font-size: 30px;
        margin-bottom: 15px;
    }
    
    .persona-title {
        font-size: 16px;
        font-weight: 600;
        color: white;
        margin-bottom: 8px;
    }
    
    .persona-desc {
        font-size: 13px;
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.4;
    }
    
    /* Chat area */
    .chat-container {
        background: transparent;
        padding: 20px 0;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .chat-message {
        margin-bottom: 15px;
        padding: 15px 20px;
        border-radius: 15px;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .chat-message.user {
        background: #00d4aa;
        margin-left: auto;
        color: white;
        border-bottom-right-radius: 5px;
    }
    
    .chat-message.model {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-right: auto;
        color: white;
        border-bottom-left-radius: 5px;
    }
    
    /* Input area */
    .input-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 10px 20px;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-top: 20px;
        position: sticky;
        bottom: 20px;
    }
    
    /* Buttons */
    .stButton > button {
        background: #00d4aa !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: #00b894 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0, 212, 170, 0.3) !important;
    }
    
    /* Voice button special styling */
    .voice-btn > button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        padding: 0 !important;
        font-size: 18px !important;
    }
    
    .voice-btn > button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
    }
    
    /* Chat input */
    .stChatInput > div > div > textarea {
        background: transparent !important;
        border: none !important;
        color: white !important;
        font-size: 16px !important;
    }
    
    .stChatInput > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Progress and status */
    .stSpinner > div {
        border-top-color: #00d4aa !important;
    }
    
    .stAlert {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    /* Sidebar content */
    .sidebar-title {
        color: white !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-bottom: 20px !important;
    }
    
    .chat-history-item {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        color: rgba(255, 255, 255, 0.8);
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .chat-history-item:hover {
        background: rgba(255, 255, 255, 0.15);
        color: white;
    }
    
    .chat-history-title {
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .chat-history-preview {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    /* Audio player styling */
    .stAudio {
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.audio_files = {}

if "pending_bot" not in st.session_state:
    st.session_state.pending_bot = False

if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_persona" not in st.session_state:
    st.session_state.current_persona = None


PERSONAS = {
    "general": {"icon": "🤖", "title": "General Assistant", "desc": "Help with general questions and tasks"},
    "creative": {"icon": "🎨", "title": "Creative Writer", "desc": "Stories, poems, and creative content"},
    "teacher": {"icon": "👨‍🏫", "title": "Teacher", "desc": "Explain concepts and help with learning"},
    "coder": {"icon": "💻", "title": "Code Helper", "desc": "Programming assistance and debugging"},
    "analyst": {"icon": "📊", "title": "Data Analyst", "desc": "Data analysis and insights"},
    "therapist": {"icon": "🧠", "title": "Life Coach", "desc": "Personal guidance and motivation"}
}

def convert_messages_for_gemini(messages, current_persona=None):
    """Convert messages to Gemini format and extract system instruction"""
    gemini_messages = []
    system_instruction = None
    
    
    if current_persona and current_persona in PERSONAS:
        persona = PERSONAS[current_persona]
        system_instruction = f"You are a {persona['title']}. {persona['desc']}. Respond accordingly."
    
    for role, content in messages:
        if role == "system":
            
            system_instruction = content
        elif role == "user":
            gemini_messages.append(("user", content))
        elif role == "ai" or role == "model":
            
            gemini_messages.append(("model", content))
        
    
    return gemini_messages, system_instruction


with st.sidebar:
    st.markdown('<h2 class="sidebar-title">MiniBot</h2>', unsafe_allow_html=True)
    
    
    if st.button("🆕 New Chat", use_container_width=True):
        
        if st.session_state.messages:
            chat_title = st.session_state.messages[0][1][:30] + "..." if len(st.session_state.messages[0][1]) > 30 else st.session_state.messages[0][1]
            st.session_state.chat_history.append({
                "title": chat_title,
                "messages": st.session_state.messages.copy(),
                "persona": st.session_state.current_persona
            })
        
        
        for audio_path in st.session_state.get("audio_files", {}).values():
            try:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except:
                pass
        
        st.session_state.messages = []
        st.session_state.audio_files = {}
        st.session_state.show_welcome = True
        st.session_state.current_persona = None
        st.session_state.pending_bot = False
        st.rerun()
    
    
    st.markdown('<h3 class="sidebar-title" style="font-size: 16px; margin-top: 30px;">Chat History</h3>', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        for i, chat in enumerate(reversed(st.session_state.chat_history[-10:])):  # Show last 10 chats
            if st.button(f"💬 {chat['title']}", key=f"history_{i}", use_container_width=True):
                st.session_state.messages = chat['messages'].copy()
                st.session_state.current_persona = chat['persona']
                st.session_state.show_welcome = False
                st.rerun()
    else:
        st.markdown("""
        <div style="color: rgba(255, 255, 255, 0.6); font-size: 14px; text-align: center; padding: 20px;">
            No chat history yet.<br>Start a conversation!
        </div>
        """, unsafe_allow_html=True)


def select_persona(persona_key):
    st.session_state.current_persona = persona_key
    st.session_state.show_welcome = False
    
    persona = PERSONAS[persona_key]
    welcome_msg = f"Hi! I'm your {persona['title']}. {persona['desc']}. How can I help you today?"
    st.session_state.messages.append(("model", welcome_msg))  # Changed from "ai" to "model"
    st.rerun()


if st.session_state.show_welcome and not st.session_state.messages:
    
    st.markdown("""
    <div class="welcome-container">
        <div class="bot-avatar">🤖</div>
        <h1 class="welcome-title">Welcome to MiniBot</h1>
        <p class="welcome-subtitle">Choose a persona to get started:</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    cols = st.columns(3)
    persona_keys = list(PERSONAS.keys())
    
    for i, (key, persona) in enumerate(PERSONAS.items()):
        col_index = i % 3
        with cols[col_index]:
            if st.button(
                f"{persona['icon']}\n\n**{persona['title']}**\n\n{persona['desc']}", 
                key=f"persona_{key}",
                use_container_width=True
            ):
                select_persona(key)

else:
    
    if st.session_state.current_persona:
        persona = PERSONAS[st.session_state.current_persona]
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; margin-bottom: 20px;">
            <span style="font-size: 24px;">{persona['icon']}</span>
            <h2 style="color: white; margin: 10px 0;">{persona['title']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for i, (role, msg) in enumerate(st.session_state.messages):
        
        display_role = "ai" if role == "model" else role
        role_class = "user" if role == "user" else "model"
        st.markdown(f'<div class="chat-message {role_class}">{msg}</div>', unsafe_allow_html=True)
        
       
        if i in st.session_state.audio_files:
            audio_file = st.session_state.audio_files[i]
            if os.path.exists(audio_file):
                st.audio(audio_file, format="audio/mp3")
    
    st.markdown('</div>', unsafe_allow_html=True)


if st.session_state.pending_bot:
    with st.spinner("MiniBot is thinking..."):
        try:
            
            gemini_messages, system_instruction = convert_messages_for_gemini(
                st.session_state.messages, 
                st.session_state.current_persona
            )
            
           
            reply = get_gemini_response(gemini_messages, system_instruction=system_instruction)
            st.session_state.messages.append(("model", reply))  
            
            
            tts = gTTS(reply)
            audio_path = os.path.join(tempfile.gettempdir(), f"mini_bot_reply_{len(st.session_state.messages)}.mp3")
            tts.save(audio_path)
            st.session_state.audio_files[len(st.session_state.messages) - 1] = audio_path
            
        except Exception as e:
            st.session_state.messages.append(("model", f"❌ Error: {e}"))  
        finally:
            st.session_state.pending_bot = False
            st.rerun()


col1, col2 = st.columns([1, 12])

with col1:
    if st.button("🎤", help="Click to speak", key="voice_btn"):
        if st.session_state.show_welcome:
            st.session_state.show_welcome = False
            st.session_state.current_persona = "general"  
            
        with st.spinner("🎧 Listening..."):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                    user_voice = recognizer.recognize_google(audio)
                    
                    if user_voice.strip():
                        st.session_state.messages.append(("user", user_voice))
                        st.session_state.pending_bot = True
                        st.rerun()
                        
                except sr.WaitTimeoutError:
                    st.error("⏱️ Timeout! Please try again.")
                except sr.UnknownValueError:
                    st.error("🤔 Sorry, I didn't catch that.")
                except sr.RequestError as e:
                    st.error(f"⚠️ Speech error: {e}")
                except Exception as e:
                    st.error(f"🎙️ Unexpected error: {e}")


with col2:
    user_text = st.chat_input("Type your message here...")
    if user_text and user_text.strip():
        if st.session_state.show_welcome:
            st.session_state.show_welcome = False
            st.session_state.current_persona = "general" 
            
        st.session_state.messages.append(("user", user_text.strip()))
        st.session_state.pending_bot = True
        st.rerun()