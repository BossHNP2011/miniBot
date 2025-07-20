import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
import google.generativeai as genai

# ----------------- LOAD ENV ------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# ----------------- CONFIG ------------------
st.set_page_config(page_title="MiniBot Gemini", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #0f172a;
    }
    .block-container {
        background-color: #0f172a;
        padding: 2rem;
        color: white;
    }
    .stButton>button {
        background-color: #1e293b;
        color: #38bdf8;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 10px;
        box-shadow: 0 0 10px #38bdf8;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #0ea5e9;
        color: white;
    }
    input[type='text'] {
        background-color: #1e293b;
        color: white;
        border-radius: 10px;
        border: 1px solid #38bdf8;
        padding: 0.75em;
    }
    .persona-button {
        padding: 1em;
        margin-top: 0.5em;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 0 8px rgba(56, 189, 248, 0.5);
        background-color: #1e293b;
        color: #38bdf8;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- API Check ------------------
if not API_KEY:
    st.error("🚨 API Key not found. Please add it to your `.env` file as GEMINI_API_KEY.")
    st.stop()

# ----------------- Gemini Setup ------------------
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# ----------------- Session State ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "persona" not in st.session_state:
    st.session_state.persona = "General"

# ----------------- SIDEBAR ------------------
with st.sidebar:
    st.markdown("## 🌐 MiniBot", unsafe_allow_html=True)
    st.markdown("<button class='persona-button'>+ New Chat</button>", unsafe_allow_html=True)
    st.markdown("#### 🧾 Chat History", unsafe_allow_html=True)
    for i, (user, bot) in enumerate(st.session_state.chat_history):
        st.markdown(f"**🧑‍💻 You:** {user}<br>**🤖 Bot:** {bot}", unsafe_allow_html=True)

# ----------------- Welcome Header ------------------
st.markdown("""
    <div style="text-align: center; padding: 2em;">
        <h2 style="color: #38bdf8;">🤖 Welcome to MiniBot</h2>
        <p style="color: #cbd5e1;">How can I assist you today?</p>
    </div>
""", unsafe_allow_html=True)

# ----------------- Persona Selection ------------------
cols = st.columns(4)
personas = ["🧠 Concept", "💻 Coding", "✍️ Writing", "📊 Analysis"]

for i in range(4):
    with cols[i]:
        if st.button(personas[i], use_container_width=True):
            st.session_state.persona = personas[i]
            st.success(f"Persona set to {personas[i]}")

st.markdown("---")

# ----------------- Chat Messages ------------------
for user, bot in st.session_state.chat_history:
    message(user, is_user=True, key=user + "_user")
    message(bot, key=bot + "_bot")

# ----------------- Chat Input ------------------
col1, col2 = st.columns([8, 1])
with col1:
    user_input = st.text_input("Type your message...", key="user_input", label_visibility="collapsed")
with col2:
    send = st.button("📤", use_container_width=True)

# ----------------- Chat Logic ------------------
if send and user_input:
    persona_prefix = {
        "🧠 Concept": "You are an expert concept explainer. Make it simple and intuitive.",
        "💻 Coding": "You are a senior programmer. Give clean and optimized code with comments.",
        "✍️ Writing": "You are a creative writer. Keep responses engaging and grammatically perfect.",
        "📊 Analysis": "You are a data analyst. Provide sharp insights and summaries."
    }

    full_prompt = f"{persona_prefix.get(st.session_state.persona, '')}\nUser: {user_input}"

    try:
        response = model.generate_content(full_prompt)
        bot_reply = response.text
        st.session_state.chat_history.append((user_input, bot_reply))
        st.session_state.user_input = ""
    except Exception as e:
        st.error(f"❌ Gemini API Error: {e}")

# ----------------- Placeholder for Mic ------------------
st.markdown("🔊 Voice input coming soon...", unsafe_allow_html=True)
