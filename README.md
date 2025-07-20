# 🌟 Mini Bot - Voice Assistant

Mini Bot is a Streamlit-powered chatbot that supports both text and voice input. It uses Google's Gemini API for intelligent responses and can read replies aloud using text-to-speech.

---

## Features

- **Conversational AI** powered by Gemini
- **Voice input** (speech-to-text)
- **Text input** (chat box)
- **Voice output** (text-to-speech playback)
- **Chat history** with audio playback for bot responses

---

## Installation

1. **Clone the repository:**
   ```
   git clone <https://github.com/sania0607/miniBot>
   cd Mini-bot
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
   Or manually:
   ```
   pip install streamlit gtts pydub speechrecognition python-dotenv google-generativeai chromadb
   ```

3. **Set up your Gemini API key:**
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

---

## Usage

1. **Run the app:**
   ```
   streamlit run app.py
   ```

2. **Interact:**
   - Type your message in the chat box at the bottom.
   - Or click "Hold to Speak" to use your microphone.
   - Bot replies will appear as chat bubbles and can be played as audio.

---

## File Structure

- `app.py` — Main Streamlit app
- `services/gemini_service.py` — Handles Gemini API calls and memory
- `components/chat_ui.py` — Chat bubble rendering and custom CSS
- `.env` — Your Gemini API key

---

## Notes

- Make sure your microphone is enabled for voice input.
- The input controls are fixed at the bottom for easy access.
- Requires Python 3.8+.

---


## Credits

- [Streamlit](https://streamlit.io/)
- [Google Gemini](https://ai.google.com/)
- [gTTS](https://pypi.org/project/gTTS/)
- [pydub](https://pypi.org/project/pydub/)




