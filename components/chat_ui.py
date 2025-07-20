# components/chat_ui.py

import streamlit as st

def inject_css():
    st.markdown("""
    <style>
        /* Gradient Background */
        body {
            background: linear-gradient(135deg, #0f172a, #1e3a8a);
        }

        section[data-testid="stSidebar"] {
            background-color: #1e293b;
            color: white;
        }

        /* Logo badge */
        .logo-top {
            position: absolute;
            top: 12px;
            right: 20px;
            font-size: 13px;
            color: #cbd5e1;
        }

        /* Center Card */
        .center-box {
            background: rgba(255, 255, 255, 0.05);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            backdrop-filter: blur(8px);
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
            margin-bottom: 2rem;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
        }

        .feature-card {
            padding: 1rem;
            border-radius: 15px;
            background-color: #1e293b;
            color: white;
            box-shadow: inset 0 0 5px #00000066;
            transition: 0.3s ease;
        }

        .feature-card:hover {
            background-color: #2563eb;
            cursor: pointer;
        }

        .chat-bubble {
            padding: 1rem;
            margin-bottom: 0.5rem;
            border-radius: 1rem;
            max-width: 80%;
        }

        .user { background-color: #334155; margin-left: auto; }
        .ai { background-color: #0369a1; margin-right: auto; }

        .chat-area {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .input-box input {
            background-color: #1e293b;
            color: white;
            border-radius: 20px;
            padding: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)


def render_chat_bubble(role, message, audio_file=None):
    css_class = "user" if role == "user" else "ai"
    st.markdown(f"<div class='chat-bubble {css_class}'>{message}</div>", unsafe_allow_html=True)
    if audio_file:
        st.audio(audio_file)
