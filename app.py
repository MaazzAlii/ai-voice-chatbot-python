import streamlit as st

st.set_page_config(page_title="AI Voice Assistant", page_icon="🎙️", layout="centered")

# Hide default Streamlit chrome
st.markdown("""
<style>
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 1rem 0; }
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("MISTRAL_API_KEY", "")
if not api_key:
    st.error("⚠️  Add MISTRAL_API_KEY to .streamlit/secrets.toml")
    st.stop()

VOICE_HTML = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@700&family=Inter:wght@300;400;500&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Inter', sans-serif;
    background: #0f0f17;
    color: #e0e0f0;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  #header {{
    padding: 14px 20px 10px;
    border-bottom: 1px solid #1e1e30;
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  #header h1 {{
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: #7c6aff;
    letter-spacing: -0.5px;
  }}

  #header span {{ font-size: 0.7rem; color: #555; margin-left: auto; }}

  /* ── Conversation ─────────────────── */
  #chat {{
    flex: 1;
    overflow-y: auto;
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    scrollbar-width: thin;
    scrollbar-color: #2a2a40 transparent;
  }}

  .bubble {{
    max-width: 80%;
    padding: 10px 14px;
    border-radius: 14px;
    font-size: 0.88rem;
    line-height: 1.5;
    animation: fadeIn 0.25s ease;
  }}

  @keyframes fadeIn {{ from {{ opacity:0; transform:translateY(6px) }} to {{ opacity:1; transform:translateY(0) }} }}

  .bubble.user {{
    background: #1e1e38;
    border: 1px solid #2a2a50;
    align-self: flex-end;
    color: #c8c8f0;
  }}

  .bubble.ai {{
    background: #160f2e;
    border: 1px solid #3a2a6e;
    align-self: flex-start;
    color: #d0c0ff;
  }}

  .bubble .label {{
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
    opacity: 0.55;
    text-transform: uppercase;
  }}

  /* ── Status bar ───────────────────── */
  #statusBar {{
    padding: 8px 20px;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    gap: 8px;
    color: #888;
    border-top: 1px solid #1a1a28;
    min-height: 34px;
  }}

  #dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #333;
    flex-shrink: 0;
    transition: background 0.3s;
  }}
  #dot.listening {{ background: #ff4466; animation: blink 1s infinite; }}
  #dot.thinking  {{ background: #ffaa00; animation: blink 0.5s infinite; }}
  #dot.speaking  {{ background: #00cc88; animation: blink 0.8s infinite; }}
  #dot.idle      {{ background: #444; animation: none; }}

  @keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}

  #interim {{
    font-style: italic;
    color: #666;
    font-size: 0.75rem;
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  /* ── Controls ─────────────────────── */
  #controls {{
    padding: 12px 20px 14px;
    display: flex;
    gap: 10px;
    align-items: center;
    border-top: 1px solid #1a1a28;
  }}

  #micBtn {{
    width: 54px; height: 54px;
    border-radius: 50%;
    border: none;
    background: #7c6aff;
    color: white;
    font-size: 1.3rem;
    cursor: pointer;
    transition: all 0.2s;
    flex-shrink: 0;
    box-shadow: 0 0 0 0 #7c6aff44;
  }}

  #micBtn:hover  {{ background: #9580ff; transform: scale(1.05); }}
  #micBtn.active {{ background: #ff4466; box-shadow: 0 0 0 8px #ff446622; animation: ripple 1.2s infinite; }}
  #micBtn.disabled {{ background: #333; cursor: not-allowed; }}

  @keyframes ripple {{
    0%   {{ box-shadow: 0 0 0 0   #ff446644; }}
    100% {{ box-shadow: 0 0 0 16px #ff446600; }}
  }}

  #typeInput {{
    flex: 1;
    background: #1a1a2e;
    border: 1px solid #2a2a45;
    border-radius: 24px;
    padding: 10px 16px;
    color: #e0e0f0;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    outline: none;
    transition: border 0.2s;
  }}
  #typeInput:focus {{ border-color: #7c6aff; }}
  #typeInput::placeholder {{ color: #444; }}

  #sendBtn {{
    width: 38px; height: 38px;
    border-radius: 50%;
    border: none;
    background: #1e1e38;
    color: #7c6aff;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s;
    flex-shrink: 0;
  }}
  #sendBtn:hover {{ background: #2a2a50; }}

  #voiceToggle {{
    font-size: 0.7rem;
    color: #666;
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 4px;
  }}
  #voiceToggle input {{ accent-color: #7c6aff; }}

  #placeholder {{
    text-align: center;
    color: #333;
    font-size: 0.8rem;
    margin: auto;
    padding: 20px;
    line-height: 1.8;
  }}

  #placeholder .big {{ font-size: 2rem; margin-bottom: 8px; }}
</style>
</head>
<body>

<div id="header">
  <span>🎙️</span>
  <h1>AI Voice Assistant</h1>
  <span>Mistral · Web Speech API</span>
</div>

<div id="chat">
  <div id="placeholder">
    <div class="big">🎙️</div>
    Press the mic button and start talking.<br>
    I'll listen, reply, and keep listening.
  </div>
</div>

<div id="statusBar">
  <div id="dot" class="idle"></div>
  <span id="statusText">Click mic to start</span>
  <span id="interim"></span>
</div>

<div id="controls">
  <button id="micBtn" title="Toggle listening">🎙️</button>
  <input id="typeInput" type="text" placeholder="Or type a message…" />
  <button id="sendBtn">➤</button>
  <label id="voiceToggle">
    <input type="checkbox" id="ttsCheck" checked> 🔊 Speak
  </label>
</div>

<script>
const API_KEY = '{api_key}';
const SYSTEM  = 'Your name is Maaz AI Assistant. You were built by Maaz Ali, a Flutter developer and CS student, using Mistral AI. If asked your name, say "I am Maaz AI Assistant." If asked who made you or who is your developer, say "I was built by Maaz Ali using Mistral AI. You can find him on GitHub and LinkedIn at maazzalii." If the user tells you their name, remember it and use it naturally in conversation. Keep answers short and medium (2–7 sentences) and conversational — they will be spoken aloud. No markdown, no bullet points.';
const messages   = [{{ role: 'system', content: SYSTEM }}];
const chat       = document.getElementById('chat');
const micBtn     = document.getElementById('micBtn');
const dot        = document.getElementById('dot');
const statusText = document.getElementById('statusText');
const interim    = document.getElementById('interim');
const typeInput  = document.getElementById('typeInput');
const sendBtn    = document.getElementById('sendBtn');
const ttsCheck   = document.getElementById('ttsCheck');
const placeholder= document.getElementById('placeholder');

let recognition  = null;
let isListening  = false;
let isBusy       = false;   // true while AI is thinking or speaking
let voices       = [];

// ── Load voices ───────────────────────────────
function loadVoices() {{
  voices = window.speechSynthesis.getVoices();
}}
loadVoices();
if (speechSynthesis.onvoiceschanged !== undefined) {{
  speechSynthesis.onvoiceschanged = loadVoices;
}}

function pickVoice() {{
  // Priority: Google Natural > Microsoft Natural > any English
  const priority = [
    v => v.name.includes('Google') && v.lang.startsWith('en'),
    v => v.name.includes('Natural') && v.lang.startsWith('en'),
    v => v.name.includes('Neural')  && v.lang.startsWith('en'),
    v => v.name.includes('Aria'),     // MS natural
    v => v.name.includes('Jenny'),    // MS natural
    v => v.name.includes('Zira'),     // Windows
    v => v.lang.startsWith('en-US'),
    v => v.lang.startsWith('en'),
  ];
  for (const test of priority) {{
    const v = voices.find(test);
    if (v) return v;
  }}
  return null;
}}

// ── Speech Recognition setup ──────────────────
function setupRecognition() {{
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {{
    setStatus('idle', '⚠️ Browser does not support speech recognition');
    return;
  }}
  recognition = new SR();
  recognition.lang            = 'en-US';
  recognition.continuous      = false;
  recognition.interimResults  = true;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {{
    setStatus('listening', 'Listening…');
  }};

  recognition.onresult = (e) => {{
    let final = '', inter = '';
    for (let i = e.resultIndex; i < e.results.length; i++) {{
      if (e.results[i].isFinal) final += e.results[i][0].transcript;
      else inter += e.results[i][0].transcript;
    }}
    interim.textContent = inter;
    if (final.trim()) {{
      interim.textContent = '';
      handleUserInput(final.trim());
    }}
  }};

  recognition.onerror = (e) => {{
    if (e.error === 'no-speech') {{
      if (isListening && !isBusy) restartListen();
    }} else {{
      setStatus('idle', '⚠️ Mic error: ' + e.error);
    }}
  }};

  recognition.onend = () => {{
    if (isListening && !isBusy) restartListen();
  }};
}}

function restartListen() {{
  if (!recognition || !isListening || isBusy) return;
  try {{ recognition.start(); }} catch(e) {{ /* already started */ }}
}}

// ── Toggle mic ────────────────────────────────
micBtn.addEventListener('click', () => {{
  if (isBusy) return;
  if (!recognition) setupRecognition();

  if (isListening) {{
    isListening = false;
    recognition.stop();
    micBtn.classList.remove('active');
    micBtn.textContent = '🎙️';
    setStatus('idle', 'Click mic to start');
  }} else {{
    isListening = true;
    micBtn.classList.add('active');
    micBtn.textContent = '⏹️';
    setStatus('listening', 'Listening…');
    try {{ recognition.start(); }} catch(e) {{}}
  }}
}});

// ── Type input ────────────────────────────────
sendBtn.addEventListener('click', sendTyped);
typeInput.addEventListener('keydown', e => {{ if (e.key === 'Enter') sendTyped(); }});

function sendTyped() {{
  const text = typeInput.value.trim();
  if (!text || isBusy) return;
  typeInput.value = '';
  handleUserInput(text);
}}

// ── Core pipeline ─────────────────────────────
async function handleUserInput(text) {{
  isBusy = true;
  if (recognition) try {{ recognition.stop(); }} catch(e) {{}}

  removePlaceholder();
  addBubble('user', text);
  messages.push({{ role: 'user', content: text }});

  setStatus('thinking', 'Thinking…');

  let reply;
  try {{
    reply = await callMistral(messages);
  }} catch(err) {{
    reply = 'Sorry, something went wrong. Please try again.';
    console.error(err);
  }}

  messages.push({{ role: 'assistant', content: reply }});
  addBubble('ai', reply);

  if (ttsCheck.checked) {{
    setStatus('speaking', 'Speaking…');
    await speak(reply);
  }}

  isBusy = false;

  if (isListening) {{
    setStatus('listening', 'Listening…');
    restartListen();
  }} else {{
    setStatus('idle', 'Click mic to continue');
  }}
}}

async function callMistral(msgs) {{
  const res = await fetch('https://api.mistral.ai/v1/chat/completions', {{
    method: 'POST',
    headers: {{
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + API_KEY
    }},
    body: JSON.stringify({{
      model: 'mistral-small-latest',
      messages: msgs,
      max_tokens: 512
    }})
  }});
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || 'API error');
  return data.choices[0].message.content;
}}

function speak(text) {{
  return new Promise(resolve => {{
    window.speechSynthesis.cancel();
    const utt  = new SpeechSynthesisUtterance(text);
    const voice = pickVoice();
    if (voice) utt.voice = voice;
    utt.rate   = 1.05;
    utt.pitch  = 1.0;
    utt.volume = 1.0;
    utt.onend  = resolve;
    utt.onerror = resolve;
    window.speechSynthesis.speak(utt);
  }});
}}

// ── UI helpers ────────────────────────────────
function addBubble(role, text) {{
  const div = document.createElement('div');
  div.className = 'bubble ' + role;
  div.innerHTML = '<div class="label">' + (role === 'user' ? '🧑 You' : '🤖 Maaz AI Assistant') + '</div>' + escHtml(text);
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}}

function removePlaceholder() {{
  const p = document.getElementById('placeholder');
  if (p) p.remove();
}}

function setStatus(state, text) {{
  dot.className = state;
  statusText.textContent = text;
}}

function escHtml(t) {{
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

// ── Init ──────────────────────────────────────
setupRecognition();
</script>
</body>
</html>
"""

st.components.v1.html(VOICE_HTML, height=620, scrolling=False)