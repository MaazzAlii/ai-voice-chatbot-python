# 🎙️Voice AI Assistant — Voice-Powered AI Chat Agent

> A real-time, browser-based voice assistant powered by **Mistral AI** and the **Web Speech API**. Talk to it — it listens, thinks, and speaks back in a natural human voice. Built with Python + Streamlit.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?style=flat-square&logo=streamlit)
![Mistral AI](https://img.shields.io/badge/Mistral_AI-API-orange?style=flat-square)
![Web Speech API](https://img.shields.io/badge/Web_Speech-API-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## ✨ Features

- 🎙️ **Always-on voice listening** — click once, it keeps listening after every reply
- 🤖 **Mistral AI backend** — fast, intelligent conversational responses
- 🔊 **Natural voice output** — uses browser's Neural TTS (Google/Microsoft voices)
- 💬 **Text input fallback** — type if you prefer
- 🧠 **Conversation memory** — remembers context across the full session
- ⚡ **Zero heavy dependencies** — no PyAudio, no C++ build tools needed
- 🌐 **Runs in the browser** — works on Windows, Mac, Linux

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM / AI** | Mistral AI (`mistral-small-latest`) |
| **Speech-to-Text** | Web Speech API (Chrome/Edge built-in) |
| **Text-to-Speech** | Web Speech Synthesis API (Neural voices) |
| **UI Framework** | Streamlit + HTML/CSS/JS component |
| **Language** | Python 3.10+ |
| **API Client** | OpenAI-compatible SDK → Mistral endpoint |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/MaazzAlii/ai-voice-chatbot-python.git
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Mistral API key

Create the file `.streamlit/secrets.toml`:
```toml
MISTRAL_API_KEY = "your_mistral_api_key_here"
```

> 🔑 Get a **free** API key at [console.mistral.ai](https://console.mistral.ai)

### 5. Run the app
```bash
streamlit run app.py
```

Open **Chrome or Edge** at `http://localhost:8501`

---

## 🎮 How to Use

1. Click the **🎙️ mic button** — turns red, starts listening
2. **Speak naturally** — auto-transcribes and replies
3. After replying, **auto-resumes listening** for your next message
4. Click **⏹️** anytime to stop
5. Toggle **🔊 Speak** to turn voice on/off
6. Or just **type** in the text box

---

## 📁 Project Structure

```
maaz-ai-assistant/
│
├── app.py                   # Main app (Streamlit + JS voice engine)
├── requirements.txt         # Python dependencies
├── .streamlit/
│   └── secrets.toml         # API key — DO NOT commit this
├── .gitignore
└── README.md
```

---

## ⚠️ Browser Compatibility

| Browser | Works? |
|---------|--------|
| ✅ Google Chrome | Full support |
| ✅ Microsoft Edge | Full support |
| ❌ Firefox | Not supported |

> Use **Google Chrome** for the best experience.

---

## 👨‍💻 Developer

**Maaz Ali** — BS Computer Science, NUML Islamabad
- 🐙 GitHub: [@maazzalii](https://github.com/maazzalii)
- 💼 LinkedIn: [maazzalii](https://linkedin.com/in/maazzalii)

---

> ⭐ Star this repo if you found it useful!
