# 🎙️ AI Voice Assistant

A full-stack voice-powered AI assistant built with Mistral AI, SpeechRecognition, pyttsx3, and Streamlit.

## Features
- 🎙️ **Microphone input** — captures voice via SpeechRecognition (Google STT, free)
- 🤖 **Mistral AI** — generates intelligent, conversational replies
- 🔊 **Text-to-speech** — speaks responses aloud via pyttsx3 (offline, no API key needed)
- 💬 **Chat UI** — full conversation history in a clean Streamlit interface
- ⌨️ **Text fallback** — also supports typed input

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> **Windows users:** If `pyaudio` fails, install it via:
> ```bash
> pip install pipwin && pipwin install pyaudio
> ```
>
> **Linux users:**
> ```bash
> sudo apt-get install portaudio19-dev python3-pyaudio
> ```

### 2. Add your Mistral API key

Get a free key at [console.mistral.ai](https://console.mistral.ai), then:

```toml
# .streamlit/secrets.toml
MISTRAL_API_KEY = "your_key_here"
```

### 3. Run

```bash
streamlit run app.py
```

## Tech Stack

| Layer | Tool |
|-------|------|
| LLM | Mistral AI (`mistral-small-latest`) |
| Speech-to-Text | SpeechRecognition + Google STT (free) |
| Text-to-Speech | pyttsx3 (offline) |
| UI | Streamlit |
| Language | Python 3.10+ |

## Project Structure

```
ai_voice_assistant/
├── app.py                  # Main application
├── requirements.txt
├── .streamlit/
│   └── secrets.toml        # API key (never commit this)
└── README.md
```

## CV Description

> **AI Voice Assistant** · Python, Mistral AI, SpeechRecognition, pyttsx3, Streamlit  
> Built a real-time voice assistant integrating speech-to-text input, Mistral LLM responses, and offline text-to-speech output in a conversational Streamlit UI with full message history.
