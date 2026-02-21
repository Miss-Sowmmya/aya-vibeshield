"""
Aya VibeShield - AI Transaction Co-Pilot
Premium Dark-Gold Fintech UI — Production Ready
Backend logic is UNCHANGED.

FIX: Side panels are rendered via components.html() inside st.columns()
instead of CSS position:fixed + st.markdown(), which caused raw HTML text
to appear. This approach renders correctly in all Streamlit versions.
"""

import streamlit as st
import random
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile

st.set_page_config(
    page_title="Aya VibeShield",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — Premium Dark Gold Theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500;600&display=swap');

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 18px 2px rgba(212,175,55,0.22); }
    50%       { box-shadow: 0 0 36px 8px rgba(212,175,55,0.42); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0);    }
}

html, body, .stApp {
    background: linear-gradient(135deg, #060911, #0c1120, #101828, #09111e, #060911) !important;
    background-size: 400% 400% !important;
    animation: gradientShift 22s ease infinite !important;
    font-family: 'Raleway', sans-serif;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }

/* Remove default column gaps and padding */
.main .block-container {
    padding-top: 1.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080c18 0%, #0e1520 100%) !important;
    border-right: 1px solid rgba(212,175,55,0.15);
}
[data-testid="stSidebar"] * { color: #c9a84c !important; font-family: 'Raleway', sans-serif !important; }

/* Title */
.aya-title {
    font-family: 'Cinzel', serif;
    font-size: clamp(1.7rem, 3vw, 2.6rem);
    font-weight: 700;
    background: linear-gradient(90deg, #7a5c10, #d4af37, #f5d97e, #d4af37, #7a5c10);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 5s linear infinite;
    letter-spacing: 0.1em;
    text-align: center;
    margin-bottom: 0.15rem;
}
.aya-caption {
    text-align: center;
    color: #6b5c28;
    font-size: 0.76rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}
.aya-info {
    background: rgba(212,175,55,0.06);
    border: 1px solid rgba(212,175,55,0.18);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    color: #a88228;
    font-size: 0.82rem;
    text-align: center;
    margin-bottom: 1.4rem;
}

/* Gold divider */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.35), transparent);
    margin: 1.3rem 0;
    border: none;
}

/* Section label */
.section-label {
    font-family: 'Cinzel', serif;
    font-size: 0.66rem;
    letter-spacing: 0.26em;
    text-transform: uppercase;
    color: #6b5c28;
    margin-bottom: 0.45rem;
    margin-top: 0.15rem;
}

/* Risk score card */
.risk-score-card {
    background: rgba(212,175,55,0.05);
    border: 1px solid rgba(212,175,55,0.22);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    text-align: center;
    animation: glowPulse 3.5s ease-in-out infinite, fadeInUp 0.5s ease both;
    margin-bottom: 1rem;
}
.risk-score-number {
    font-family: 'Cinzel', serif;
    font-size: clamp(2.8rem, 5vw, 4.2rem);
    font-weight: 700;
    background: linear-gradient(135deg, #c9a020, #f5d97e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.risk-score-label {
    font-size: 0.7rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #6b5c28;
    margin-top: 0.35rem;
    font-family: 'Raleway', sans-serif;
}

/* Risk meter */
.risk-meter-wrap {
    background: rgba(255,255,255,0.05);
    border-radius: 50px;
    height: 7px;
    overflow: hidden;
    margin: 0.85rem 0 0.65rem;
}
.risk-meter-fill { height: 100%; border-radius: 50px; }

/* Badge */
.risk-badge {
    display: inline-block;
    padding: 0.32rem 1.4rem;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.8rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-family: 'Raleway', sans-serif;
    margin-top: 0.45rem;
    animation: fadeInUp 0.4s ease both;
}
.risk-high   { background: rgba(210,50,50,0.13);  border: 1px solid rgba(210,50,50,0.45);  color: #ee7070; }
.risk-medium { background: rgba(212,175,55,0.11); border: 1px solid rgba(212,175,55,0.38); color: #d4af37; }
.risk-low    { background: rgba(45,190,90,0.09);  border: 1px solid rgba(45,190,90,0.38);  color: #58cc7e; }

/* Explanation box */
.explanation-box {
    background: rgba(212,175,55,0.045);
    border-left: 3px solid rgba(212,175,55,0.32);
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1.1rem;
    color: #c0982a;
    font-size: 0.88rem;
    line-height: 1.65;
    margin-bottom: 1rem;
    animation: fadeInUp 0.45s ease both;
}

/* Factor items */
.factor-item {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    padding: 0.48rem 0.85rem;
    margin: 0.32rem 0;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(212,175,55,0.09);
    border-radius: 8px;
    color: #917538;
    font-size: 0.84rem;
    animation: fadeInUp 0.5s ease both;
}
.factor-dot {
    width: 6px; height: 6px;
    min-width: 6px;
    background: #d4af37;
    border-radius: 50%;
    margin-top: 0.38rem;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(8,11,20,0.85) !important;
    border: 1px solid rgba(212,175,55,0.22) !important;
    border-radius: 10px !important;
    color: #e0c86a !important;
    font-family: 'Raleway', sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: rgba(212,175,55,0.55) !important;
    box-shadow: 0 0 0 2px rgba(212,175,55,0.1) !important;
}

/* Labels */
label, .stRadio label p, .stNumberInput label,
.stTextInput label, .stCheckbox label {
    color: #6b5c28 !important;
    font-family: 'Raleway', sans-serif !important;
    font-size: 0.76rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #7a5c10, #d4af37, #b8921e) !important;
    color: #06090f !important;
    font-family: 'Cinzel', serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.14em !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.65rem 2.2rem !important;
    width: 100% !important;
    box-shadow: 0 4px 22px rgba(212,175,55,0.22) !important;
    transition: all 0.28s ease !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 30px rgba(212,175,55,0.48) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Radio */
.stRadio > div { gap: 0.4rem; }
.stRadio label { color: #917538 !important; font-family: 'Raleway', sans-serif !important; }

/* Checkbox */
.stCheckbox label { color: #6b5c28 !important; font-size: 0.82rem !important; }

/* Alert */
.stAlert { border-radius: 10px !important; font-family: 'Raleway', sans-serif !important; }

/* Graph */
.graph-wrap {
    border: 1px solid rgba(212,175,55,0.16);
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 1rem;
}

/* Footer */
.aya-footer {
    text-align: center;
    color: #3e3310;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    margin-top: 1.6rem;
    font-family: 'Raleway', sans-serif;
}

/* Remove iframe border from components.html */
iframe { border: none !important; }
</style>
""",
            unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PANEL HTML TEMPLATES
# Rendered via components.html() inside columns — avoids raw-text rendering.
# ─────────────────────────────────────────────────────────────────────────────

USER_PANEL_HTML = """<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Raleway:wght@400;500&display=swap');
  @keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
  @keyframes softPulse { 0%,100%{opacity:0.5;transform:scale(1)} 50%{opacity:1;transform:scale(1.2)} }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:transparent;font-family:'Raleway',sans-serif}
  .card{
    background:rgba(10,13,22,0.85);
    backdrop-filter:blur(20px);
    border:1px solid rgba(212,175,55,0.18);
    border-radius:18px;
    padding:1.3rem 1rem;
    animation:fadeIn 0.5s ease both;
    box-shadow:0 8px 32px rgba(0,0,0,0.6),inset 0 1px 0 rgba(212,175,55,0.07);
  }
  .avatar-wrap{text-align:center;margin-bottom:0.7rem}
  .avatar{
    width:58px;height:58px;border-radius:50%;
    border:2px solid rgba(212,175,55,0.45);
    background:#110e03;
    display:inline-flex;align-items:center;justify-content:center;
    font-family:'Cinzel',serif;font-size:1.4rem;color:#d4af37;
    box-shadow:0 0 18px rgba(212,175,55,0.22);
  }
  .name{font-family:'Cinzel',serif;font-size:0.85rem;color:#d4af37;text-align:center;letter-spacing:0.09em;margin-bottom:0.12rem}
  .sub{font-size:0.66rem;color:#6b5c28;text-align:center;letter-spacing:0.18em;text-transform:uppercase;margin-bottom:0.85rem}
  .divider{height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.22),transparent);margin:0.65rem 0}
  .section-title{font-family:'Cinzel',serif;font-size:0.58rem;letter-spacing:0.24em;text-transform:uppercase;color:#4a3d1a;margin-bottom:0.45rem}
  .stat-row{display:flex;align-items:center;gap:0.45rem;padding:0.36rem 0.1rem;font-size:0.73rem;color:#a08030;border-bottom:1px solid rgba(212,175,55,0.06)}
  .stat-row:last-child{border-bottom:none}
  .dot-on{width:7px;height:7px;border-radius:50%;background:#5ecf80;box-shadow:0 0 5px rgba(94,207,128,0.6);flex-shrink:0}
  .dot-gold{width:7px;height:7px;border-radius:50%;background:#d4af37;box-shadow:0 0 5px rgba(212,175,55,0.55);animation:softPulse 2.5s infinite ease-in-out;flex-shrink:0}
</style>
</head>
<body>
<div class="card">
  <div class="avatar-wrap"><div class="avatar">A</div></div>
  <div class="name">Aya User</div>
  <div class="sub">Shield Active</div>
  <div class="section-title">Security Status</div>
  <div class="stat-row"><div class="dot-on"></div>Wallet Shield: ON</div>
  <div class="stat-row"><div class="dot-on"></div>AI Monitor: Running</div>
  <div class="stat-row"><div class="dot-gold"></div>Risk Guard: Enabled</div>
  <div class="stat-row"><div class="dot-gold"></div>Network: Ethereum</div>
  <div class="divider"></div>
  <div class="section-title">Session</div>
  <div class="stat-row"><div class="dot-on"></div>Connected</div>
  <div class="stat-row"><div class="dot-gold"></div>Mode: Secured</div>
</div>
</body>
</html>"""

INTEL_PANEL_HTML = """<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Raleway:wght@400;500&display=swap');
  @keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
  @keyframes softPulse { 0%,100%{opacity:0.45;transform:scale(1)} 50%{opacity:1;transform:scale(1.22)} }
  @keyframes scanLine { 0%{top:0%} 100%{top:100%} }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:transparent;font-family:'Raleway',sans-serif}
  .card{
    background:rgba(10,13,22,0.85);
    backdrop-filter:blur(20px);
    border:1px solid rgba(212,175,55,0.18);
    border-radius:18px;
    padding:1.3rem 1rem;
    animation:fadeIn 0.5s ease both;
    box-shadow:0 8px 32px rgba(0,0,0,0.6),inset 0 1px 0 rgba(212,175,55,0.07);
    position:relative;overflow:hidden;
  }
  .card::after{
    content:'';position:absolute;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,rgba(212,175,55,0.1),transparent);
    animation:scanLine 7s linear infinite;pointer-events:none;
  }
  .live-header{display:flex;align-items:center;gap:0.45rem;font-family:'Cinzel',serif;font-size:0.6rem;letter-spacing:0.26em;text-transform:uppercase;color:#6b5c28;margin-bottom:0.85rem}
  .live-dot{width:8px;height:8px;border-radius:50%;background:#d4af37;box-shadow:0 0 8px rgba(212,175,55,0.7);animation:softPulse 2s infinite ease-in-out;flex-shrink:0}
  .divider{height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.2),transparent);margin:0.65rem 0}
  .section-title{font-family:'Cinzel',serif;font-size:0.58rem;letter-spacing:0.24em;text-transform:uppercase;color:#4a3d1a;margin-bottom:0.45rem}
  .intel-row{display:flex;align-items:center;gap:0.45rem;padding:0.36rem 0.1rem;font-size:0.73rem;color:#917538;border-bottom:1px solid rgba(212,175,55,0.06)}
  .intel-row:last-child{border-bottom:none}
  .dot-ok{width:7px;height:7px;border-radius:50%;background:#5ecf80;box-shadow:0 0 5px rgba(94,207,128,0.55);flex-shrink:0}
  .dot-warn{width:7px;height:7px;border-radius:50%;background:#d4af37;box-shadow:0 0 5px rgba(212,175,55,0.55);flex-shrink:0}
  .gauge-wrap{background:rgba(255,255,255,0.04);border-radius:50px;height:5px;overflow:hidden;margin:0.28rem 0 0.55rem}
  .gauge-fill{height:100%;border-radius:50px}
  .gauge-label{display:flex;justify-content:space-between;font-size:0.63rem;color:#5a4820}
</style>
</head>
<body>
<div class="card">
  <div class="live-header"><div class="live-dot"></div>Live Threat Intel</div>
  <div class="intel-row"><div class="dot-ok"></div>Pattern scanner active</div>
  <div class="intel-row"><div class="dot-ok"></div>Contract monitor live</div>
  <div class="intel-row"><div class="dot-ok"></div>Behavior model warm</div>
  <div class="intel-row"><div class="dot-ok"></div>Oracle sync: OK</div>
  <div class="intel-row"><div class="dot-warn"></div>Gas anomaly: none</div>
  <div class="divider"></div>
  <div class="section-title">Network Load</div>
  <div class="gauge-wrap"><div class="gauge-fill" style="width:38%;background:linear-gradient(90deg,#7a5c10,#d4af37)"></div></div>
  <div class="gauge-label"><span>ETH Mainnet</span><span>38%</span></div>
  <div class="gauge-wrap" style="margin-top:0.35rem"><div class="gauge-fill" style="width:22%;background:linear-gradient(90deg,#1a6b3a,#58cc7e)"></div></div>
  <div class="gauge-label"><span>Risk Index</span><span>Low</span></div>
  <div class="divider"></div>
  <div class="section-title">AI Engine</div>
  <div class="intel-row"><div class="dot-ok"></div>Heuristic model: v2.1</div>
  <div class="intel-row"><div class="dot-ok"></div>Inference: 14ms</div>
  <div class="intel-row"><div class="dot-warn"></div>Aya Guard: Standby</div>
</div>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# BACKEND — UNCHANGED
# ─────────────────────────────────────────────────────────────────────────────
def analyze_wallet(address, amount):
    base = random.randint(20, 80)
    if amount > 5:
        base += 10
    if address.startswith("0x"):
        base -= 5
    if len(address) < 20:
        base += 15
    score = max(1, min(base, 100))
    if score > 70:
        level = "High Risk"
        msg_simple = "This transaction looks risky. Beginners should avoid sending funds."
        msg_expert = "Risk signals detected based on wallet pattern and transaction size."
    elif score > 40:
        level = "Medium Risk"
        msg_simple = "This might be safe, but double-check before sending."
        msg_expert = "Moderate risk based on heuristic analysis."
    else:
        level = "Low Risk"
        msg_simple = "This transaction appears safe."
        msg_expert = "Low risk profile detected."
    return score, level, msg_simple, msg_expert


def create_graph():
    G = nx.Graph()
    G.add_edge("User Wallet", "Aya Smart Guard")
    G.add_edge("Aya Smart Guard", "Target Contract")
    G.add_edge("Target Contract", "Risk Oracle")
    net = Network(height="420px",
                  width="100%",
                  bgcolor="#060911",
                  font_color="#d4af37",
                  directed=True)
    net.barnes_hut(gravity=-20000,
                   central_gravity=0.3,
                   spring_length=150,
                   spring_strength=0.05)
    net.toggle_physics(True)
    net.set_options("""
    {
      "nodes": {
        "color": {
          "border": "#d4af37",
          "background": "#1a1507",
          "highlight": { "border": "#f5d97e", "background": "#2a2010" }
        },
        "font": { "size": 13 }
      },
      "edges": { "color": { "color": "#7a6930", "highlight": "#d4af37" }, "width": 1.5 },
      "physics": {
        "stabilization": { "iterations": 120, "fit": true },
        "barnesHut": { "gravitationalConstant": -8000, "springLength": 200 }
      }
    }
    """)
    net.from_nx(G)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(tmp.name)
    return tmp.name


# ─────────────────────────────────────────────────────────────────────────────
# THREE-COLUMN LAYOUT
# Left/right panels use components.html() — eliminates raw-HTML-text bug.
# ─────────────────────────────────────────────────────────────────────────────
col_left, col_main, col_right = st.columns([1, 2.8, 1], gap="medium")

# ── LEFT PANEL ───────────────────────────────────────────────────────────────
with col_left:
    components.html(USER_PANEL_HTML, height=400, scrolling=False)

# ── MAIN COLUMN ──────────────────────────────────────────────────────────────
with col_main:

    st.markdown('<div class="aya-title">AYA VIBESHIELD</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="aya-caption">AI Transaction Co-Pilot &nbsp;|&nbsp; Aya Multi-Chain Wallet</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="aya-info">Pre-transaction intelligence layer designed for the Aya multi-chain wallet ecosystem.</div>',
        unsafe_allow_html=True,
    )

    # Inputs
    wallet = st.text_input("Enter Wallet Address",
                           help="Supports EVM-compatible wallet formats.")
    amount = st.number_input("Transaction Amount (ETH)", min_value=0.0)
    mode = st.radio("User Mode", ["Beginner", "Expert"], horizontal=True)
    st.checkbox("Simulate Aya Wallet Integration (preview feature)")

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    # CTA
    if st.button("Predict Transaction Risk"):
        if wallet:
            score, level, simple, expert = analyze_wallet(wallet, amount)

            # Risk score card
            st.markdown(f"""
            <div class="risk-score-card">
                <div class="risk-score-number">{score}</div>
                <div class="risk-score-label">Risk Score</div>
            </div>
            """,
                        unsafe_allow_html=True)

            # Meter + badge
            if score > 70:
                bar_color = "linear-gradient(90deg, #c9a020, #e05050)"
                badge_cls = "risk-high"
            elif score > 40:
                bar_color = "linear-gradient(90deg, #7a5c10, #d4af37)"
                badge_cls = "risk-medium"
            else:
                bar_color = "linear-gradient(90deg, #1a6b3a, #58cc7e)"
                badge_cls = "risk-low"

            st.markdown(f"""
            <div class="risk-meter-wrap">
                <div class="risk-meter-fill" style="width:{score}%; background:{bar_color};"></div>
            </div>
            <div style="text-align:center;">
                <span class="risk-badge {badge_cls}">{level}</span>
            </div>
            """,
                        unsafe_allow_html=True)

            st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

            # AI Explanation
            st.markdown('<div class="section-label">AI Explanation</div>',
                        unsafe_allow_html=True)
            explanation = simple if mode == "Beginner" else expert
            st.markdown(f'<div class="explanation-box">{explanation}</div>',
                        unsafe_allow_html=True)

            # Risk Factors
            st.markdown(
                '<div class="section-label">Risk Factors Detected</div>',
                unsafe_allow_html=True)
            factors = []
            if amount > 5:
                factors.append("Large transaction amount detected")
            if len(wallet) < 20:
                factors.append("Wallet address length appears unusual")
            if wallet.startswith("0x"):
                factors.append("EVM-compatible wallet pattern recognized")
            if not factors:
                factors.append("No major heuristic risks detected")

            factors_html = "".join(
                f'<div class="factor-item"><div class="factor-dot"></div><span>{f}</span></div>'
                for f in factors)
            st.markdown(factors_html, unsafe_allow_html=True)

            st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

            # Trust Graph
            st.markdown('<div class="section-label">Trust Graph</div>',
                        unsafe_allow_html=True)
            html_path = create_graph()
            with open(html_path, "r", encoding="utf-8") as fh:
                graph_html = fh.read()

            st.markdown('<div class="graph-wrap">', unsafe_allow_html=True)
            components.html(graph_html, height=430)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(
                '<div class="aya-footer">Future: Direct integration with Aya Wallet for real-time protection.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning("Please enter a wallet address to analyze.")

# ── RIGHT PANEL ───────────────────────────────────────────────────────────────
with col_right:
    components.html(INTEL_PANEL_HTML, height=500, scrolling=False)
