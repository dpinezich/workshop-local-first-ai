<script setup>
import { ref, onMounted, nextTick } from 'vue'

const messages = ref([])          // { role, content, backend }
const input = ref('')
const busy = ref(false)
const mode = ref('chat')          // 'chat' | 'rag'
const features = ref({ uploads: false, cloud: false, local_model: '…' })
const chatEl = ref(null)

// Hell/Dunkel wie bei den Folien: Dunkel ist Standard (Beamer), ?theme=light oder der Knopf
// oben rechts schaltet um, die Wahl bleibt im localStorage. Taste T tut dasselbe.
const theme = ref('dark')
function applyTheme(t) {
  theme.value = t
  if (t === 'light') document.documentElement.dataset.theme = 'light'
  else delete document.documentElement.dataset.theme
  try { localStorage.setItem('theme', t) } catch {}
}
function toggleTheme() { applyTheme(theme.value === 'light' ? 'dark' : 'light') }

// Verlauf leeren – nach einem Test wieder bei null anfangen. Das Modell merkt sich nichts,
// der ganze Verlauf steckt nur in diesem Array (Kapitel 3: kein Gedächtnis).
function clearChat() { messages.value = [] }

onMounted(async () => {
  const fromUrl = new URLSearchParams(location.search).get('theme')
  let saved = null
  try { saved = localStorage.getItem('theme') } catch {}
  applyTheme(fromUrl || saved || 'dark')
  addEventListener('keydown', e => {
    if (e.key.toLowerCase() === 't' && !['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement?.tagName)) toggleTheme()
  })
  try { features.value = await (await fetch('/api/features')).json() } catch {}
})

// Minimales Markdown fuer Modell-Antworten: fett, Titel, Listen, Code. Bewusst klein –
// die Teilnehmer sollen die rohe Antwort erkennen, nicht ein Rendering-Framework bedienen.
function md(text) {
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  return esc(text)
    .replace(/^#{1,6}\s+(.+)$/gm, '<strong>$1</strong>')
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^\s*[-*]\s+/gm, '  • ')
    .replace(/^---+$/gm, '')
}

function scrollDown() {
  nextTick(() => { if (chatEl.value) chatEl.value.scrollTop = chatEl.value.scrollHeight })
}

async function send() {
  const text = input.value.trim()
  if (!text || busy.value) return
  input.value = ''
  messages.value.push({ role: 'user', content: text })
  busy.value = true
  scrollDown()
  try {
    if (mode.value === 'rag') await askRag(text)
    else await askChat(text)
  } catch (e) {
    messages.value.push({ role: 'assistant', content: 'Fehler: ' + e.message, backend: 'error' })
  }
  busy.value = false
  scrollDown()
}

async function askChat(text) {
  const history = messages.value.map(m => ({ role: m.role, content: m.content }))
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages: history })
  })
  const backend = res.headers.get('X-Backend') || 'local'
  const msg = { role: 'assistant', content: '', backend }
  messages.value.push(msg)
  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    msg.content += decoder.decode(value, { stream: true })
    scrollDown()
  }
}

async function askRag(text) {
  const res = await fetch('/api/rag/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: text })
  })
  if (!res.ok) throw new Error((await res.json()).detail || res.statusText)
  const data = await res.json()
  const sources = data.sources.map(s => `${s.name} (${s.score})`).join(', ')
  messages.value.push({
    role: 'assistant',
    content: data.answer + '\n\n📄 Quellen: ' + sources,
    backend: 'local'
  })
}

async function uploadAudio(ev) {
  const file = ev.target.files[0]
  if (!file) return
  busy.value = true
  messages.value.push({ role: 'user', content: '🎙️ ' + file.name })
  const form = new FormData()
  form.append('file', file)
  try {
    const res = await fetch('/api/transcribe', { method: 'POST', body: form })
    if (!res.ok) throw new Error((await res.json()).detail || res.statusText)
    const data = await res.json()
    messages.value.push({ role: 'assistant', backend: 'local',
      content: `Transkript (${data.seconds}s):\n\n${data.text}` })
  } catch (e) {
    messages.value.push({ role: 'assistant', content: 'Fehler: ' + e.message, backend: 'error' })
  }
  busy.value = false
  ev.target.value = ''
  scrollDown()
}

async function uploadImage(ev) {
  const file = ev.target.files[0]
  if (!file) return
  busy.value = true
  messages.value.push({ role: 'user', content: '🖼️ ' + file.name })
  const form = new FormData()
  form.append('file', file)
  try {
    const res = await fetch('/api/vision', { method: 'POST', body: form })
    if (!res.ok) throw new Error((await res.json()).detail || res.statusText)
    const data = await res.json()
    messages.value.push({ role: 'assistant', content: data.description, backend: 'local' })
  } catch (e) {
    messages.value.push({ role: 'assistant', content: 'Fehler: ' + e.message, backend: 'error' })
  }
  busy.value = false
  ev.target.value = ''
  scrollDown()
}
</script>

<template>
  <div class="app">
    <header>
      <h1>Local-First AI Stack</h1>
      <div class="meta">
        <span class="pill local">lokal: {{ features.local_model }}</span>
        <span class="pill" :class="features.cloud ? 'cloud' : 'off'">
          cloud: {{ features.cloud ? 'bereit' : 'aus' }}
        </span>
        <label class="mode">
          <select v-model="mode">
            <option value="chat">💬 Chat (Router entscheidet)</option>
            <option value="rag">📚 Dokumente fragen (RAG)</option>
          </select>
        </label>
        <button class="theme" @click="clearChat" :disabled="busy || messages.length === 0" title="Chat löschen">🗑️</button>
        <button class="theme" @click="toggleTheme" :title="theme === 'light' ? 'Dunkel (T)' : 'Hell (T)'">
          {{ theme === 'light' ? '🌙' : '☀️' }}
        </button>
      </div>
    </header>

    <main ref="chatEl">
      <p v-if="messages.length === 0" class="empty">
        Frag etwas – der Router entscheidet, ob lokal oder Cloud antwortet.<br />
        Im RAG-Modus: Frag z.B. nach <em>«Wie viele Tage Urlaub habe ich?»</em>
      </p>
      <div v-for="(m, i) in messages" :key="i" class="msg" :class="m.role">
        <div class="bubble">
          <span v-if="m.role === 'assistant' && m.backend" class="badge" :class="m.backend">
            {{ m.backend === 'local' ? '🖥️ lokal' : m.backend === 'cloud' ? '☁️ cloud' : '⚠️' }}
          </span>
          <pre v-html="md(m.content)"></pre>
        </div>
      </div>
      <div v-if="busy" class="msg assistant"><div class="bubble typing">●●●</div></div>
    </main>

    <footer>
      <template v-if="features.uploads">
        <label class="iconbtn" :class="{ off: busy }" title="Audio transkribieren">
          🎙️<input type="file" accept="audio/*" @change="uploadAudio" :disabled="busy" hidden />
        </label>
        <label class="iconbtn" :class="{ off: busy }" title="Bild analysieren">
          🖼️<input type="file" accept="image/*" @change="uploadImage" :disabled="busy" hidden />
        </label>
      </template>
      <input v-model="input" @keyup.enter="send" :disabled="busy"
             placeholder="Nachricht… (Enter zum Senden)" />
      <button @click="send" :disabled="busy || !input.trim()">Senden</button>
    </footer>
  </div>
</template>

<style>
/* Farben wie die Folien (admin/slides): Dunkel = Standard, Hell über data-theme="light" am <html>. */
:root {
  --bg: #0f1a1d; --panel: #16282d; --panel-2: #1c3238; --line: #2a4a52; --line-soft: #1f3439;
  --text: #e8eef0; --muted: #94a8ad; --dim: #6b7f85;
  --teal: #4dc3cf; --teal-strong: #0e8c99; --lokal: #6fd3a7; --cloud: #7fb8f0; --red: #f08a7f;
  --user-bubble: #0e4a52; --bold: #ffffff;
}
:root[data-theme="light"] {
  --bg: #f2f6f7; --panel: #ffffff; --panel-2: #e6eef0; --line: #c3d3d7; --line-soft: #d9e4e7;
  --text: #10262b; --muted: #4f6a71; --dim: #7a9096;
  --teal: #0e8c99; --teal-strong: #0e8c99; --lokal: #1f9a6a; --cloud: #2b6fd1; --red: #c8553f;
  --user-bubble: #d5eef0; --bold: #10262b;
}
* { box-sizing: border-box; margin: 0; }
body { font-family: -apple-system, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); }
.app { display: flex; flex-direction: column; height: 100vh; max-width: 860px; margin: 0 auto; }
header { padding: 16px 20px; border-bottom: 1px solid var(--line-soft); }
h1 { font-size: 18px; color: var(--teal); }
.meta { display: flex; gap: 8px; margin-top: 8px; align-items: center; flex-wrap: wrap; }
.pill { font-size: 12px; padding: 2px 10px; border-radius: 999px; border: 1px solid var(--line); }
.pill.local { color: var(--lokal); } .pill.cloud { color: var(--cloud); } .pill.off { color: var(--dim); }
.mode select { background: var(--panel); color: var(--text); border: 1px solid var(--line); border-radius: 8px; padding: 4px 8px; }
.theme { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 2px 8px; font-size: 14px; cursor: pointer; line-height: 1.6; }
.theme:first-of-type { margin-left: auto; }
.theme:disabled { opacity: 0.35; cursor: default; }
main { flex: 1; overflow-y: auto; padding: 20px; }
.empty { color: var(--dim); text-align: center; margin-top: 40px; line-height: 1.7; }
.msg { display: flex; margin-bottom: 12px; }
.msg.user { justify-content: flex-end; }
.bubble { max-width: 78%; padding: 10px 14px; border-radius: 14px; background: var(--panel); }
:root[data-theme="light"] .bubble { border: 1px solid var(--line-soft); }
.msg.user .bubble { background: var(--user-bubble); }
.bubble pre { white-space: pre-wrap; word-break: break-word; font: inherit; }
.badge { display: inline-block; font-size: 11px; margin-bottom: 6px; padding: 1px 8px; border-radius: 999px; background: var(--bg); }
.badge.local { color: var(--lokal); } .badge.cloud { color: var(--cloud); } .badge.error { color: var(--red); }
.typing { color: var(--teal); letter-spacing: 3px; }
footer { display: flex; gap: 8px; padding: 14px 20px; border-top: 1px solid var(--line-soft); }
footer input[type="text"], footer input:not([type]) { flex: 1; background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 10px 14px; color: var(--text); font-size: 15px; }
footer button { background: var(--teal-strong); border: 0; color: white; border-radius: 10px; padding: 0 20px; font-size: 15px; cursor: pointer; }
footer button:disabled { opacity: 0.4; cursor: default; }
.iconbtn { font-size: 20px; cursor: pointer; align-self: center; }
.iconbtn.off { opacity: 0.35; pointer-events: none; }
.bubble b { color: var(--bold); } .bubble strong { display: block; color: var(--teal); margin-top: 6px; } .bubble code { font-family: ui-monospace, Menlo, monospace; font-size: 13px; background: var(--bg); padding: 1px 5px; border-radius: 4px; }
</style>
