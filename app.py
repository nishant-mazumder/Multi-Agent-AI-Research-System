import streamlit as st
import time
import threading
from io import StringIO
from pipeline import run_research_pipeline

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroResearch · AI Pipeline",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  –  Dark Glassmorphism + Neon
# ─────────────────────────────────────────────
GLOBAL_CSS = """
<style>
/* ── Google Fonts ───────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── CSS Variables ───────────────────────────── */
:root {
  --bg-void:        #04050a;
  --bg-deep:        #080c14;
  --bg-card:        rgba(12, 18, 35, 0.72);
  --bg-card-hover:  rgba(16, 26, 52, 0.85);
  --border-dim:     rgba(80, 120, 255, 0.15);
  --border-glow:    rgba(80, 160, 255, 0.45);
  --neon-blue:      #4fc3f7;
  --neon-purple:    #b085f5;
  --neon-cyan:      #00e5ff;
  --neon-green:     #69ffb4;
  --neon-pink:      #f06292;
  --text-primary:   #e8eaf6;
  --text-secondary: #8892b0;
  --text-muted:     #4a5568;
  --grad-accent:    linear-gradient(135deg, #4fc3f7 0%, #b085f5 100%);
  --grad-card:      linear-gradient(145deg, rgba(79,195,247,0.06) 0%, rgba(176,133,245,0.04) 100%);
  --shadow-card:    0 8px 32px rgba(0,0,0,0.6), 0 0 0 1px rgba(79,195,247,0.08);
  --shadow-glow:    0 0 40px rgba(79,195,247,0.18), 0 8px 48px rgba(0,0,0,0.7);
}

/* ── Base Reset ─────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg-void) !important;
  color: var(--text-primary) !important;
  font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%, rgba(79,195,247,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 85%, rgba(176,133,245,0.07) 0%, transparent 55%),
    radial-gradient(ellipse 50% 60% at 50% 50%, rgba(0,229,255,0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* ── Sidebar ────────────────────────────────── */
[data-testid="stSidebar"] {
  background: rgba(6, 9, 20, 0.96) !important;
  border-right: 1px solid var(--border-dim) !important;
  backdrop-filter: blur(20px) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Main container ─────────────────────────── */
.main .block-container {
  padding: 2rem 3rem !important;
  max-width: 1100px !important;
}

/* ── Typography ─────────────────────────────── */
h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }

/* ── Streamlit widget overrides ─────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  background: rgba(10, 16, 32, 0.8) !important;
  border: 1px solid var(--border-dim) !important;
  border-radius: 12px !important;
  color: var(--text-primary) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.95rem !important;
  padding: 0.75rem 1rem !important;
  transition: all 0.3s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--neon-blue) !important;
  box-shadow: 0 0 0 3px rgba(79,195,247,0.15) !important;
}

/* ── Buttons ────────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, #1a6bcc 0%, #7c3aed 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 12px !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
  padding: 0.7rem 2rem !important;
  letter-spacing: 0.04em !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 0 4px 24px rgba(79,195,247,0.25) !important;
  cursor: pointer !important;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 8px 32px rgba(79,195,247,0.4) !important;
  background: linear-gradient(135deg, #2280e0 0%, #8b5cf6 100%) !important;
}
.stButton > button:active { transform: translateY(0) scale(0.99) !important; }

/* ── Expander ────────────────────────────────── */
[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-dim) !important;
  border-radius: 16px !important;
  backdrop-filter: blur(16px) !important;
  box-shadow: var(--shadow-card) !important;
  margin-bottom: 1rem !important;
  overflow: hidden !important;
  transition: all 0.3s ease !important;
}
[data-testid="stExpander"]:hover {
  border-color: var(--border-glow) !important;
  box-shadow: var(--shadow-glow) !important;
}
[data-testid="stExpander"] summary {
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  font-size: 1.05rem !important;
  padding: 1.1rem 1.4rem !important;
  color: var(--text-primary) !important;
}

/* ── Progress bar ─────────────────────────────── */
.stProgress > div > div {
  background: var(--grad-accent) !important;
  border-radius: 99px !important;
  box-shadow: 0 0 12px rgba(79,195,247,0.5) !important;
}

/* ── Spinner ──────────────────────────────────── */
[data-testid="stSpinner"] {
  color: var(--neon-blue) !important;
}

/* ── Code / markdown in outputs ───────────────── */
[data-testid="stMarkdown"] code {
  background: rgba(79,195,247,0.08) !important;
  color: var(--neon-cyan) !important;
  border-radius: 4px !important;
  font-family: 'JetBrains Mono', monospace !important;
}

/* ── Divider ─────────────────────────────────── */
hr { border-color: var(--border-dim) !important; }

/* ── Animations ───────────────────────────────── */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
  0%, 100% { box-shadow: 0 0 20px rgba(79,195,247,0.2); }
  50%       { box-shadow: 0 0 40px rgba(79,195,247,0.5); }
}
@keyframes gradientShift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

.fade-in-up { animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) both; }
.fade-in-up-d1 { animation: fadeInUp 0.6s 0.1s cubic-bezier(0.4, 0, 0.2, 1) both; }
.fade-in-up-d2 { animation: fadeInUp 0.6s 0.2s cubic-bezier(0.4, 0, 0.2, 1) both; }
.fade-in-up-d3 { animation: fadeInUp 0.6s 0.3s cubic-bezier(0.4, 0, 0.2, 1) both; }
.fade-in-up-d4 { animation: fadeInUp 0.6s 0.4s cubic-bezier(0.4, 0, 0.2, 1) both; }

/* ── Custom Components ─────────────────────────── */
.hero-header {
  text-align: center;
  padding: 3rem 1rem 2rem;
  animation: fadeInUp 0.8s ease both;
}
.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: clamp(2.2rem, 5vw, 3.4rem);
  font-weight: 800;
  background: linear-gradient(135deg, #4fc3f7 0%, #b085f5 55%, #f06292 100%);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 4s ease infinite;
  line-height: 1.15;
  margin-bottom: 0.6rem;
}
.hero-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.92rem;
  color: var(--text-secondary);
  letter-spacing: 0.06em;
}

.glass-card {
  background: var(--bg-card);
  border: 1px solid var(--border-dim);
  border-radius: 20px;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  box-shadow: var(--shadow-card);
  padding: 1.8rem 2rem;
  transition: all 0.3s ease;
}
.glass-card:hover {
  border-color: var(--border-glow);
  box-shadow: var(--shadow-glow);
  transform: translateY(-2px);
}

.step-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(79,195,247,0.1);
  border: 1px solid rgba(79,195,247,0.3);
  border-radius: 99px;
  padding: 4px 14px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  color: var(--neon-blue);
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}
.step-badge.done {
  background: rgba(105,255,180,0.1);
  border-color: rgba(105,255,180,0.3);
  color: var(--neon-green);
}
.step-badge.active {
  animation: pulseGlow 1.6s ease infinite;
}

.status-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 1.2rem 0 1.6rem;
}
.status-chip {
  flex: 1;
  min-width: 140px;
  background: rgba(10, 16, 32, 0.7);
  border: 1px solid var(--border-dim);
  border-radius: 12px;
  padding: 0.7rem 1rem;
  text-align: center;
  font-family: 'Syne', sans-serif;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted);
  transition: all 0.4s ease;
}
.status-chip.pending  { color: var(--text-muted); }
.status-chip.active   { color: var(--neon-blue);  border-color: rgba(79,195,247,0.5); background: rgba(79,195,247,0.07); animation: pulseGlow 1.6s ease infinite; }
.status-chip.done     { color: var(--neon-green); border-color: rgba(105,255,180,0.4); background: rgba(105,255,180,0.06); }
.status-chip.error    { color: var(--neon-pink);  border-color: rgba(240,98,146,0.4); background: rgba(240,98,146,0.06); }

.output-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-secondary);
  margin-bottom: 0.4rem;
}
.output-content {
  background: rgba(4, 8, 18, 0.6);
  border: 1px solid var(--border-dim);
  border-radius: 12px;
  padding: 1.2rem 1.4rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.86rem;
  line-height: 1.8;
  color: var(--text-primary);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 380px;
  overflow-y: auto;
}
.output-content::-webkit-scrollbar { width: 5px; }
.output-content::-webkit-scrollbar-track { background: transparent; }
.output-content::-webkit-scrollbar-thumb { background: rgba(79,195,247,0.25); border-radius: 4px; }

.report-content {
  background: rgba(4, 8, 18, 0.6);
  border: 1px solid rgba(176,133,245,0.2);
  border-radius: 14px;
  padding: 1.6rem 1.8rem;
  font-family: 'Syne', sans-serif;
  font-size: 0.96rem;
  line-height: 1.9;
  color: var(--text-primary);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 500px;
  overflow-y: auto;
}
.report-content::-webkit-scrollbar { width: 5px; }
.report-content::-webkit-scrollbar-track { background: transparent; }
.report-content::-webkit-scrollbar-thumb { background: rgba(176,133,245,0.3); border-radius: 4px; }

.critic-content {
  background: rgba(4, 8, 18, 0.6);
  border: 1px solid rgba(105,255,180,0.18);
  border-radius: 14px;
  padding: 1.4rem 1.6rem;
  font-family: 'Syne', sans-serif;
  font-size: 0.94rem;
  line-height: 1.85;
  color: var(--text-primary);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 400px;
  overflow-y: auto;
}
.critic-content::-webkit-scrollbar { width: 5px; }
.critic-content::-webkit-scrollbar-track { background: transparent; }
.critic-content::-webkit-scrollbar-thumb { background: rgba(105,255,180,0.25); border-radius: 4px; }

.loading-card {
  background: var(--bg-card);
  border: 1px solid rgba(79,195,247,0.25);
  border-radius: 20px;
  backdrop-filter: blur(18px);
  padding: 2.5rem 2rem;
  text-align: center;
  animation: pulseGlow 2s ease infinite;
}
.loading-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--neon-blue);
  margin: 0.8rem 0 0.3rem;
}
.loading-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  color: var(--text-secondary);
}
.cursor {
  display: inline-block;
  width: 2px;
  height: 1em;
  background: var(--neon-blue);
  margin-left: 2px;
  vertical-align: middle;
  animation: blink 1s step-end infinite;
}

.metric-row {
  display: flex;
  gap: 12px;
  margin-bottom: 1.6rem;
  flex-wrap: wrap;
}
.metric-chip {
  flex: 1;
  min-width: 100px;
  background: rgba(10, 16, 32, 0.6);
  border: 1px solid var(--border-dim);
  border-radius: 12px;
  padding: 0.9rem 1rem;
  text-align: center;
}
.metric-num {
  font-family: 'Syne', sans-serif;
  font-size: 1.5rem;
  font-weight: 800;
  background: var(--grad-accent);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.metric-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--text-secondary);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.error-card {
  background: rgba(240, 98, 146, 0.08);
  border: 1px solid rgba(240, 98, 146, 0.35);
  border-radius: 16px;
  padding: 1.4rem 1.6rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88rem;
  color: #ff8fb1;
  animation: fadeInUp 0.5s ease both;
}

.copy-btn-area { display: flex; gap: 10px; margin-top: 1rem; flex-wrap: wrap; }

/* ── Sidebar custom ────────────────────────────── */
.sidebar-logo {
  font-family: 'Syne', sans-serif;
  font-size: 1.4rem;
  font-weight: 800;
  background: linear-gradient(135deg, #4fc3f7, #b085f5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.2rem;
}
.sidebar-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  color: var(--text-muted);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 1.4rem;
}
.sidebar-section {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--text-secondary);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin: 1.2rem 0 0.5rem;
  border-bottom: 1px solid var(--border-dim);
  padding-bottom: 0.4rem;
}
.agent-pill {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0.6rem 0.8rem;
  border-radius: 10px;
  margin-bottom: 0.4rem;
  background: rgba(79,195,247,0.05);
  border: 1px solid rgba(79,195,247,0.1);
  font-family: 'Syne', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
}
.agent-icon { font-size: 1rem; }
.agent-desc {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--text-secondary);
}

/* ── Streamlit overrides ───────────────────────── */
label { color: var(--text-secondary) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.82rem !important; letter-spacing: 0.06em !important; }
[data-testid="stMarkdown"] p { color: var(--text-primary) !important; font-family: 'Syne', sans-serif !important; }
.stAlert { border-radius: 12px !important; }
</style>
"""

# ─────────────────────────────────────────────
#  HELPER: INJECT HTML SAFELY
# ─────────────────────────────────────────────
def html(content: str, key: str | None = None):
    st.markdown(content, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        html("""
        <div style="padding: 0.5rem 0 0.2rem;">
          <div class="sidebar-logo">🧬 NeuroResearch</div>
          <div class="sidebar-tag">Multi-Agent AI Pipeline · v2.0</div>
        </div>
        """)

        st.divider()
        html('<div class="sidebar-section">System Architecture</div>')

        agents = [
            ("🔍", "Search Agent",   "Discovers & ranks sources"),
            ("📄", "Reader Agent",   "Deep-scrapes best URLs"),
            ("✍️", "Writer Chain",  "Synthesizes final report"),
            ("🧠", "Critic Chain",   "Reviews & scores output"),
        ]
        for icon, name, desc in agents:
            html(f"""
            <div class="agent-pill">
              <span class="agent-icon">{icon}</span>
              <div>
                <div>{name}</div>
                <div class="agent-desc">{desc}</div>
              </div>
            </div>
            """)

        html('<div class="sidebar-section" style="margin-top:1.6rem;">Session Stats</div>')

        runs = st.session_state.get("total_runs", 0)
        html(f"""
        <div class="metric-row" style="flex-direction:column; gap:8px;">
          <div class="metric-chip">
            <div class="metric-num">{runs}</div>
            <div class="metric-label">Total Runs</div>
          </div>
        </div>
        """)

        st.divider()
        html("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem;
                    color:var(--text-muted); line-height:1.7; padding:0.4rem 0;">
          Powered by LangGraph · LangChain<br>
          Built with Streamlit 🎈
        </div>
        """)


# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
def render_hero():
    html("""
    <div class="hero-header">
      <div class="hero-title">AI Research Intelligence</div>
      <div class="hero-sub">
        ⟶ &nbsp;Multi-agent pipeline · Real-time search · Autonomous synthesis &nbsp;⟵
      </div>
    </div>
    """)


# ─────────────────────────────────────────────
#  STATUS TRACKER
# ─────────────────────────────────────────────
STEPS = [
    ("🔍", "Search Agent"),
    ("📄", "Reader Agent"),
    ("✍️", "Writer Chain"),
    ("🧠", "Critic Chain"),
]

def render_status_tracker(active_step: int = -1, completed: int = -1):
    chips = ""
    for i, (icon, name) in enumerate(STEPS):
        if i < completed:
            cls = "done"
            prefix = "✓"
        elif i == active_step:
            cls = "active"
            prefix = "⟳"
        else:
            cls = "pending"
            prefix = str(i + 1)
        chips += f'<div class="status-chip {cls}">{prefix} {icon} {name}</div>'

    html(f'<div class="status-row">{chips}</div>')


# ─────────────────────────────────────────────
#  INPUT CARD
# ─────────────────────────────────────────────
def render_input_card():
    html('<div class="glass-card fade-in-up" style="margin-bottom:1.6rem;">')
    html("""
    <div style="font-family:'Syne',sans-serif; font-size:1.15rem; font-weight:700;
                color:var(--neon-blue); margin-bottom:0.3rem;">
      ⬡ &nbsp;Research Query
    </div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.78rem;
                color:var(--text-secondary); margin-bottom:1rem;">
      Enter any topic — the pipeline will autonomously search, read, write & review.
    </div>
    """)

    col1, col2 = st.columns([5, 1])
    with col1:
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025...",
            key="topic_input",
            label_visibility="collapsed",
        )
    with col2:
        run_clicked = st.button("▶ Run", use_container_width=True, key="run_btn")

    html("</div>")
    return topic, run_clicked


# ─────────────────────────────────────────────
#  LOADING CARD
# ─────────────────────────────────────────────
def render_loading(step_idx: int):
    messages = [
        "🔍 &nbsp;Search Agent scanning the web...",
        "📄 &nbsp;Reader Agent scraping top sources...",
        "✍️ &nbsp;Writer Chain drafting your report...",
        "🧠 &nbsp;Critic Chain reviewing quality...",
    ]
    msg = messages[step_idx] if step_idx < len(messages) else "⚙️ &nbsp;Processing..."
    html(f"""
    <div class="loading-card fade-in-up" style="margin-bottom:1.2rem;">
      <div style="font-size:2.2rem; margin-bottom:0.6rem;">
        {'⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'[step_idx % 10]}
      </div>
      <div class="loading-title">{msg}<span class="cursor"></span></div>
      <div class="loading-sub">Step {step_idx + 1} of 4 · AI agents collaborating in real-time</div>
    </div>
    """)


# ─────────────────────────────────────────────
#  RESULT SECTIONS
# ─────────────────────────────────────────────
def render_search_results(content: str):
    with st.expander("🔍  Search Agent Output", expanded=False):
        html(f"""
        <div class="fade-in-up">
          <div class="step-badge done">✓ &nbsp;STEP 1 · COMPLETE</div>
          <div class="output-label" style="margin-top:0.8rem;">Raw Search Intelligence</div>
          <div class="output-content">{content}</div>
        </div>
        """)


def render_scraped_content(content: str):
    with st.expander("📄  Scraped Web Data", expanded=False):
        html(f"""
        <div class="fade-in-up-d1">
          <div class="step-badge done">✓ &nbsp;STEP 2 · COMPLETE</div>
          <div class="output-label" style="margin-top:0.8rem; color:var(--neon-purple);">Deep Extracted Content</div>
          <div class="output-content" style="border-color:rgba(176,133,245,0.2);">{content}</div>
        </div>
        """)


def render_report(content: str):
    with st.expander("✍️  Final AI Report", expanded=True):
        html(f"""
        <div class="fade-in-up-d2">
          <div class="step-badge done" style="background:rgba(176,133,245,0.1); border-color:rgba(176,133,245,0.35); color:var(--neon-purple);">
            ✓ &nbsp;STEP 3 · COMPLETE
          </div>
          <div class="output-label" style="margin-top:0.8rem; color:var(--neon-purple);">Synthesized Research Report</div>
          <div class="report-content">{content}</div>
        </div>
        """)

        # Action buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("📋 Copy Report", key="copy_btn", use_container_width=True):
                st.session_state["copy_triggered"] = True
                st.toast("📋 Report copied to clipboard!", icon="✅")
        with col2:
            txt_bytes = content.encode("utf-8")
            st.download_button(
                "⬇ Download .txt",
                data=txt_bytes,
                file_name="neuro_research_report.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_btn",
            )

        # JS clipboard copy
        if st.session_state.get("copy_triggered"):
            escaped = content.replace("`", "\\`").replace("\\", "\\\\")
            html(f"""
            <script>
              (function() {{
                try {{
                  navigator.clipboard.writeText(`{escaped}`);
                }} catch(e) {{
                  const ta = document.createElement('textarea');
                  ta.value = `{escaped}`;
                  document.body.appendChild(ta);
                  ta.select();
                  document.execCommand('copy');
                  document.body.removeChild(ta);
                }}
              }})();
            </script>
            """)
            st.session_state["copy_triggered"] = False


def render_critic_feedback(content: str):
    with st.expander("🧠  Critic Review & Feedback", expanded=True):
        html(f"""
        <div class="fade-in-up-d3">
          <div class="step-badge done" style="background:rgba(105,255,180,0.08); border-color:rgba(105,255,180,0.35); color:var(--neon-green);">
            ✓ &nbsp;STEP 4 · COMPLETE
          </div>
          <div class="output-label" style="margin-top:0.8rem; color:var(--neon-green);">Quality Assessment</div>
          <div class="critic-content">{content}</div>
        </div>
        """)


def render_completion_banner(topic: str):
    html(f"""
    <div class="glass-card fade-in-up" style="
      border-color:rgba(105,255,180,0.35);
      background:rgba(105,255,180,0.04);
      text-align:center;
      margin-bottom:1.6rem;
      padding:1.6rem 2rem;
    ">
      <div style="font-size:1.8rem; margin-bottom:0.4rem;">🎉</div>
      <div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; color:var(--neon-green);">
        Research Complete
      </div>
      <div style="font-family:'JetBrains Mono',monospace; font-size:0.8rem; color:var(--text-secondary); margin-top:0.3rem;">
        All 4 agents finished · Topic: <span style="color:var(--neon-cyan);">"{topic}"</span>
      </div>
    </div>
    """)


# ─────────────────────────────────────────────
#  ERROR CARD
# ─────────────────────────────────────────────
def render_error(err: Exception):
    html(f"""
    <div class="error-card">
      <strong>⚠ Pipeline Error</strong><br><br>
      {str(err)}<br><br>
      <span style="color:var(--text-secondary);">
        Check your API keys, network connection, and pipeline configuration.
        See terminal logs for full traceback.
      </span>
    </div>
    """)


# ─────────────────────────────────────────────
#  MAIN PIPELINE RUNNER
# ─────────────────────────────────────────────
def run_pipeline(topic: str):
    """Runs the pipeline with step-by-step UI feedback."""

    results_placeholder = st.empty()
    progress_bar        = st.progress(0, text="Initializing agents...")
    status_placeholder  = st.empty()
    loader_placeholder  = st.empty()

    step_labels = [
        "Search Agent scanning the web…",
        "Reader Agent scraping top sources…",
        "Writer Chain drafting report…",
        "Critic Chain reviewing output…",
    ]

    try:
        # ── We intercept pipeline stages by monkey-patching print or running inline ──
        # Since pipeline.py uses print() to demarcate steps, we run the pipeline
        # directly and update UI pre/post each logical stage using a wrapper approach.

        # STEP 1 — show loading
        progress_bar.progress(5, text=step_labels[0])
        with status_placeholder:
            render_status_tracker(active_step=0, completed=-1)
        with loader_placeholder:
            render_loading(0)

        # Run full pipeline (blocking) — state dict returned
        # For step-wise feedback we run it all at once (terminal already handles steps)
        # and render as results come back.
        state = run_research_pipeline(topic)

        # ── After pipeline completes, render step-by-step with delays for UX ──

        # STEP 1 done
        progress_bar.progress(25, text="✓ Search complete · " + step_labels[1])
        with status_placeholder:
            render_status_tracker(active_step=1, completed=1)
        with loader_placeholder:
            render_loading(1)
        time.sleep(0.3)

        # STEP 2 done
        progress_bar.progress(55, text="✓ Scraping complete · " + step_labels[2])
        with status_placeholder:
            render_status_tracker(active_step=2, completed=2)
        with loader_placeholder:
            render_loading(2)
        time.sleep(0.3)

        # STEP 3 done
        progress_bar.progress(80, text="✓ Report drafted · " + step_labels[3])
        with status_placeholder:
            render_status_tracker(active_step=3, completed=3)
        with loader_placeholder:
            render_loading(3)
        time.sleep(0.3)

        # ALL DONE
        progress_bar.progress(100, text="✅ All agents complete!")
        time.sleep(0.4)
        progress_bar.empty()
        loader_placeholder.empty()

        with status_placeholder:
            render_status_tracker(active_step=-1, completed=4)

        # ── Render results ──
        render_completion_banner(topic)
        render_search_results(str(state.get("search_results", "")))
        render_scraped_content(str(state.get("scraped_content", "")))
        render_report(str(state.get("report", "")))
        render_critic_feedback(str(state.get("feedback", "")))

        # Store metrics
        st.session_state["last_result"] = state
        st.session_state["total_runs"]  = st.session_state.get("total_runs", 0) + 1
        st.session_state["last_topic"]  = topic

    except Exception as e:
        progress_bar.empty()
        loader_placeholder.empty()
        with status_placeholder:
            render_status_tracker(active_step=-1, completed=-1)
        render_error(e)
        raise


# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
def init_session():
    defaults = {
        "total_runs":       0,
        "last_result":      None,
        "last_topic":       "",
        "copy_triggered":   False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
def main():
    # Inject CSS
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    init_session()
    render_sidebar()
    render_hero()

    # Input
    topic, run_clicked = render_input_card()

    # Idle status chips
    if not run_clicked:
        render_status_tracker(active_step=-1, completed=-1)

    # Run
    if run_clicked:
        if not topic or not topic.strip():
            html("""
            <div class="error-card" style="margin-top:0.5rem;">
              ⚠ Please enter a research topic before running the pipeline.
            </div>
            """)
        else:
            run_pipeline(topic.strip())

    # Show previous results if re-rendered without clicking Run
    elif st.session_state.get("last_result") and st.session_state.get("last_topic"):
        state = st.session_state["last_result"]
        topic = st.session_state["last_topic"]

        render_status_tracker(active_step=-1, completed=4)
        render_completion_banner(topic)
        render_search_results(str(state.get("search_results", "")))
        render_scraped_content(str(state.get("scraped_content", "")))
        render_report(str(state.get("report", "")))
        render_critic_feedback(str(state.get("feedback", "")))


if __name__ == "__main__":
    main()
