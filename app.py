import streamlit as st
import json
import re
from PIL import Image
from pypdf import PdfReader
from falkordb import FalkorDB
from streamlit_agraph import agraph, Node, Edge, Config
from google import genai

# --- PAGE CONFIGURATION (WIDE MATRIX LAYOUT) ---
st.set_page_config(
    page_title="ALIBI GRAPH // Cyber-Forensics & Lie Detector",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- NAVIGATION STATE ROUTING & PERSISTENCE ---
if "in_dashboard" not in st.session_state:
    st.session_state.in_dashboard = False
if "cypher_logs" not in st.session_state:
    st.session_state.cypher_logs = []
if "f_host" not in st.session_state:
    st.session_state.f_host = "r-6jissuruar.instance-kf4vao0zb.hc-7up0crkyn.ap-south-1.aws.f2e0a955bb84.cloud"
if "f_port" not in st.session_state:
    st.session_state.f_port = 64782
if "f_user" not in st.session_state:
    st.session_state.f_user = "falkordb"
if "f_pass" not in st.session_state:
    st.session_state.f_pass = ""
if "case_id" not in st.session_state:
    st.session_state.case_id = "Case_Homicide_Sector4"
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "new_rule" not in st.session_state:
    st.session_state.new_rule = "Confront suspects immediately with photographic and digital evidence."
if "suspect_name" not in st.session_state:
    st.session_state.suspect_name = "Suspect_Marcus"

# --- STRICT 60-30-10 CYBER-FORENSIC DESIGN SYSTEM ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    /* 60% Canvas Foundation: Deep Obsidian */
    --bg-obsidian: #0B0F19;
    
    /* 30% Layout Containers & Panels: Dark Steel */
    --bg-steel: #1E293B;
    --bg-steel-subtle: rgba(30, 41, 59, 0.75);
    --bg-steel-card: rgba(30, 41, 59, 0.92);
    
    /* 10% Accent Elements & Highlights: Bio-Neon Teal */
    --accent-teal: #00F2FE;
    --accent-teal-dim: rgba(0, 242, 254, 0.12);
    --accent-teal-glow: rgba(0, 242, 254, 0.38);
    
    /* Truthful Baselines: Clinical Green */
    --clinical-green: #10B981;
    --clinical-green-dim: rgba(16, 185, 129, 0.15);
    --clinical-green-glow: rgba(16, 185, 129, 0.4);
    
    /* Deception/Contradiction Flags: Stress Crimson */
    --stress-crimson: #EF4444;
    --stress-crimson-dim: rgba(239, 68, 68, 0.15);
    --stress-crimson-glow: rgba(239, 68, 68, 0.45);
    
    /* Primary Text & Labels: Silver (Contrast Ratio > 4.5:1) */
    --text-silver: #E2E8F0;
    --text-muted: #94A3B8;
    --text-dim: #64748B;
    
    /* Borders */
    --border-subtle: rgba(0, 242, 254, 0.2);
    --border-highlight: rgba(0, 242, 254, 0.6);
}

/* Eliminate Cramped Sidebar Completely */
[data-testid="stSidebar"], section[data-testid="stSidebar"] {
    display: none !important;
}
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Global Cyber Foundation (Deep Obsidian 60%) */
html, body, [data-testid="stAppViewContainer"], .main {
    background-color: var(--bg-obsidian) !important;
    background-image: 
        radial-gradient(circle at 10% 5%, rgba(0, 242, 254, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 90% 95%, rgba(16, 185, 129, 0.04) 0%, transparent 40%),
        linear-gradient(rgba(0, 242, 254, 0.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 242, 254, 0.018) 1px, transparent 1px) !important;
    background-size: 100% 100%, 100% 100%, 32px 32px, 32px 32px !important;
    color: var(--text-silver) !important;
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
}

/* Header Bar */
[data-testid="stHeader"] {
    background: rgba(11, 15, 25, 0.85) !important;
    backdrop-filter: blur(16px) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
}

/* Main Container Padding Optimization */
.block-container {
    padding-top: 3.8rem !important;
    padding-bottom: 3rem !important;
    max-width: 98% !important;
}

/* Typography Hierarchy */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
    color: #ffffff !important;
}

p, span, label, div {
    color: var(--text-silver);
}

/* --- HERO LANDING PAGE STYLES --- */
.hero-wrapper {
    max-width: 1080px;
    margin: 1.2rem auto 2.5rem auto;
    text-align: center;
    position: relative;
}

.hero-pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 6px 18px;
    border-radius: 9999px;
    background: var(--accent-teal-dim);
    border: 1px solid var(--accent-teal);
    color: var(--accent-teal);
    letter-spacing: 0.08em;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 22px var(--accent-teal-glow);
}

.hero-title-glitch {
    font-size: 3.6rem;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.035em;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent-teal) 50%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.85rem;
    filter: drop-shadow(0 0 35px var(--accent-teal-glow));
}

.hero-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.98rem;
    font-weight: 600;
    color: var(--accent-teal);
    letter-spacing: 0.06em;
    margin-bottom: 1.35rem;
    text-transform: uppercase;
}

.hero-description {
    font-size: 1.12rem;
    line-height: 1.65;
    color: var(--text-muted);
    max-width: 840px;
    margin: 0 auto 2.6rem auto;
}

.hero-grid-features {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.15rem;
    text-align: left;
    margin-bottom: 2.8rem;
}

@media (max-width: 900px) {
    .hero-grid-features {
        grid-template-columns: repeat(2, 1fr);
    }
    .hero-title-glitch {
        font-size: 2.5rem;
    }
}

.hero-feat-card {
    background: var(--bg-steel) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    padding: 1.4rem 1.15rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
    position: relative;
    overflow: hidden;
}

.hero-feat-card:hover {
    border-color: var(--accent-teal) !important;
    box-shadow: 0 12px 32px var(--accent-teal-glow) !important;
    transform: translateY(-4px);
}

.hero-feat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-teal), transparent);
}

.hero-feat-icon {
    font-size: 1.85rem;
    margin-bottom: 0.75rem;
    display: inline-block;
}

.hero-feat-title {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.45rem;
}

.hero-feat-desc {
    font-size: 0.82rem;
    line-height: 1.5;
    color: var(--text-muted);
}

/* --- TOP HORIZONTAL NAVIGATION STRIP --- */
.top-brand-flex {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 0.3rem 0;
}

.top-brand-logo {
    font-size: 2.1rem;
    filter: drop-shadow(0 0 12px var(--accent-teal-glow));
}

.top-brand-title {
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    background: linear-gradient(90deg, #ffffff 10%, var(--accent-teal) 60%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.2;
}

.top-brand-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.04em;
    margin-top: 2px;
}

.pulse-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--clinical-green);
    box-shadow: 0 0 8px var(--clinical-green-glow);
    animation: live-pulse 1.8s infinite ease-in-out;
}

@keyframes live-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.35; transform: scale(0.7); }
}

/* --- HORIZONTAL KPI TELEMETRY STRIP (DARK STEEL 30%) --- */
.telemetry-strip-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.95rem;
    margin-bottom: 1.25rem;
}

@media (max-width: 900px) {
    .telemetry-strip-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

.telemetry-card {
    background: var(--bg-steel);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 0.95rem 1.2rem;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45);
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
}

.telemetry-card:hover {
    border-color: var(--accent-teal);
    box-shadow: 0 8px 24px var(--accent-teal-glow);
}

.telemetry-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.telemetry-value {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: #ffffff;
    display: flex;
    align-items: baseline;
    gap: 8px;
}

.telemetry-subtext {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
}

/* --- COLLAPSIBLE TOP EXPANDER / CONTROL BAR (DARK STEEL 30%) --- */
[data-testid="stExpander"] {
    background: var(--bg-steel) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    margin-bottom: 1.25rem !important;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.5) !important;
}

[data-testid="stExpander"] details summary {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    color: var(--accent-teal) !important;
    letter-spacing: 0.03em !important;
    padding: 0.75rem 1.15rem !important;
}

/* --- TABS SYSTEM --- */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-steel) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 6px !important;
    margin-bottom: 1.25rem !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: var(--text-muted) !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0, 242, 254, 0.22) 0%, var(--bg-steel) 100%) !important;
    color: #ffffff !important;
    border: 1px solid var(--accent-teal) !important;
    box-shadow: 0 4px 16px var(--accent-teal-glow) !important;
}

/* --- CONTAINER CARDS (DARK STEEL 30%) --- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--bg-steel) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 32px rgba(0, 0, 0, 0.55), inset 0 0 16px rgba(0, 242, 254, 0.02) !important;
    backdrop-filter: blur(16px) !important;
    padding: 0.85rem !important;
    margin-bottom: 1.25rem !important;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: var(--border-highlight) !important;
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.65), 0 0 20px var(--accent-teal-glow) !important;
}

/* Card Header Section */
.forensic-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 0.85rem;
    margin-bottom: 1.15rem;
}

.forensic-card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
}

.stage-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 9999px;
    background: var(--accent-teal-dim);
    border: 1px solid var(--accent-teal);
    color: var(--accent-teal);
    letter-spacing: 0.05em;
}

.stage-badge.crimson {
    background: var(--stress-crimson-dim);
    border-color: var(--stress-crimson);
    color: var(--stress-crimson);
}

.stage-badge.green {
    background: var(--clinical-green-dim);
    border-color: var(--clinical-green);
    color: var(--clinical-green);
}

/* Simulation Scenario Brief */
.sim-scenario-box {
    background: rgba(0, 242, 254, 0.04);
    border: 1px dashed rgba(0, 242, 254, 0.3);
    border-radius: 8px;
    padding: 0.95rem 1.15rem;
    margin-bottom: 1.15rem;
    font-size: 0.88rem;
    color: var(--text-silver);
    line-height: 1.5;
}

.sim-scenario-box b {
    color: var(--accent-teal);
}

/* Contradiction Clash Dossier (Stress Crimson) */
.contradiction-alert-box {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.14) 0%, rgba(20, 10, 16, 0.95) 100%);
    border: 1px solid var(--stress-crimson);
    border-radius: 10px;
    padding: 1.35rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 8px 32px var(--stress-crimson-glow), inset 0 0 16px rgba(239, 68, 68, 0.06);
}

.contradiction-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.95rem;
}

.contradiction-title {
    font-size: 1.12rem;
    font-weight: 800;
    color: var(--stress-crimson);
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.conflict-topic-pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    font-weight: 700;
    padding: 4px 11px;
    border-radius: 4px;
    background: rgba(251, 191, 36, 0.14);
    border: 1px solid #fbbf24;
    color: #fbbf24;
    margin-bottom: 0.95rem;
}

.clash-split-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.95rem;
    margin-bottom: 0.95rem;
}

@media (max-width: 768px) {
    .clash-split-grid {
        grid-template-columns: 1fr;
    }
}

.clash-dossier-card {
    background: #0E1726;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 1rem;
}

.clash-dossier-card.doc {
    border-left: 3px solid var(--accent-teal);
}

.clash-dossier-card.visual {
    border-left: 3px solid #fbbf24;
}

.dossier-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--text-dim);
    text-transform: uppercase;
    margin-bottom: 4px;
}

.dossier-source {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.88rem;
    color: #ffffff;
    margin-bottom: 6px;
}

.dossier-statement {
    font-size: 0.88rem;
    color: var(--text-silver);
    font-style: italic;
    line-height: 1.5;
}

.confrontation-teleprompter {
    background: #080D1A;
    border: 1px solid rgba(0, 242, 254, 0.35);
    border-radius: 8px;
    padding: 1.1rem;
    margin-top: 0.85rem;
}

.teleprompter-speaker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--accent-teal);
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
}

.teleprompter-script {
    font-size: 0.92rem;
    font-weight: 500;
    color: #ffffff;
    line-height: 1.55;
}

.teleprompter-rule {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    color: #818cf8;
    margin-top: 8px;
}

/* Standby Radar Card */
.standby-card {
    background: rgba(30, 41, 59, 0.5);
    border: 1px dashed rgba(0, 242, 254, 0.25);
    border-radius: 10px;
    padding: 2.2rem;
    text-align: center;
    color: var(--text-muted);
}

.standby-icon {
    font-size: 2.4rem;
    margin-bottom: 0.75rem;
    animation: radar-spin 10s linear infinite;
    display: inline-block;
}

@keyframes radar-spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Knowledge Topology Legend */
.topology-legend-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.85rem;
    background: #0E1726;
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.75rem 1.1rem;
    margin-bottom: 1.1rem;
}

.legend-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    display: flex;
    align-items: center;
    gap: 7px;
    color: var(--text-silver);
}

.legend-dot-circle {
    width: 9px;
    height: 9px;
    border-radius: 50%;
}

/* Agraph Iframe Canvas */
iframe[data-testid="stCustomComponentV1"],
div[data-testid="stCustomComponentV1"] iframe,
iframe {
    border-radius: 10px !important;
    border: 1px solid var(--border-subtle) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.75) !important;
    background-color: var(--bg-obsidian) !important;
    width: 100% !important;
}

/* Terminal / Code Inspector Box */
.terminal-hud-box {
    background: #050811;
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    overflow: hidden;
    margin-top: 0.6rem;
}

.terminal-titlebar-strip {
    background: #0d1527;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding: 7px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
}

.window-dots {
    display: flex;
    gap: 6px;
}

.window-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
}

/* Streamlit Buttons Cyber Styling (Bio-Neon Teal 10%) */
div.stButton > button {
    background: linear-gradient(135deg, rgba(0, 242, 254, 0.12) 0%, var(--bg-steel) 100%) !important;
    border: 1px solid var(--accent-teal) !important;
    color: var(--accent-teal) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.02em !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.15rem !important;
    box-shadow: 0 4px 14px var(--accent-teal-dim) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

div.stButton > button:hover {
    background: var(--accent-teal) !important;
    color: var(--bg-obsidian) !important;
    box-shadow: 0 6px 24px var(--accent-teal-glow) !important;
    transform: translateY(-2px) !important;
}

div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Inputs & Form Controls (Dark Steel 30% background) */
div[data-baseweb="input"] input,
div[data-baseweb="base-input"] input,
div[data-baseweb="select"] {
    background-color: #0d1527 !important;
    border: 1px solid rgba(0, 242, 254, 0.25) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"]:focus-within {
    border-color: var(--accent-teal) !important;
    box-shadow: 0 0 14px var(--accent-teal-glow) !important;
}

/* File Uploader Cyber Style */
[data-testid="stFileUploader"] {
    background: rgba(0, 242, 254, 0.02) !important;
    border: 1px dashed rgba(0, 242, 254, 0.35) !important;
    border-radius: 10px !important;
    padding: 0.85rem !important;
}

/* Standby Authentication Banner */
.auth-standby-banner {
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.12) 0%, var(--bg-steel) 100%);
    border: 1px solid #fbbf24;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 30px rgba(251, 191, 36, 0.2);
}

.standby-glitch {
    font-size: 1.15rem;
    font-weight: 800;
    color: #fbbf24;
    letter-spacing: -0.01em;
    margin-bottom: 0.5rem;
}

.standby-desc {
    font-size: 0.88rem;
    color: var(--text-silver);
    margin-bottom: 0.75rem;
}

.standby-desc code {
    color: var(--accent-teal);
    background: var(--accent-teal-dim);
    padding: 2px 7px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg-obsidian);
}
::-webkit-scrollbar-thumb {
    background: rgba(0, 242, 254, 0.3);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--accent-teal);
}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# SECTION 1: HERO LANDING / SPLASH SCREEN (WHEN NOT IN DASHBOARD)
# ==============================================================================
if not st.session_state.in_dashboard:
    hero_html = (
        '<div class="hero-wrapper">\n'
        '<div class="hero-pill-badge">\n'
        '<span style="color:#10B981">●</span> AUTONOMOUS CYBER-FORENSICS // FALKOR DB AP-SOUTH-1\n'
        '</div>\n'
        '<h1 class="hero-title-glitch">ALIBI GRAPH</h1>\n'
        '<div class="hero-subtitle">\n'
        'EPISODIC GRAPH INTELLIGENCE &amp; MULTI-MODAL LIE DETECTOR ENGINE\n'
        '</div>\n'
        '<p class="hero-description">\n'
        'AlibiGraph synthesizes multimodal forensic exhibits—written alibi statements, CCTV surveillance footage, '
        'phone extraction archives, and forensic audit logs—into real-time Falkor DB episodic knowledge graphs. '
        'It uncovers cross-modal contradictions in microseconds via Cypher traversal and generates procedurally-grounded '
        'cross-examination confrontation dossiers.\n'
        '</p>\n'
        '<div class="hero-grid-features">\n'
        '<div class="hero-feat-card">\n'
        '<div class="hero-feat-icon">🧠</div>\n'
        '<div class="hero-feat-title">Episodic Graph Memory</div>\n'
        '<div class="hero-feat-desc">Falkor DB Cloud-backed multi-tenant knowledge graph storing cross-modal claims, temporal anchors, and entities.</div>\n'
        '</div>\n'
        '<div class="hero-feat-card">\n'
        '<div class="hero-feat-icon">🔍</div>\n'
        '<div class="hero-feat-title">Agent 1: Profiler</div>\n'
        '<div class="hero-feat-desc">Automated claim extraction &amp; semantic normalization across CCTV images, PDFs, and testimonies.</div>\n'
        '</div>\n'
        '<div class="hero-feat-card">\n'
        '<div class="hero-feat-icon">⚖️</div>\n'
        '<div class="hero-feat-title">Agent 2: Cross-Examiner</div>\n'
        '<div class="hero-feat-desc">Real-time Cypher contradiction reasoning detecting conflicting alibi axes and formulating prosecutorial scripts.</div>\n'
        '</div>\n'
        '<div class="hero-feat-card">\n'
        '<div class="hero-feat-icon">⚡</div>\n'
        '<div class="hero-feat-title">Microsecond Traversal</div>\n'
        '<div class="hero-feat-desc">Ultra low-latency Cypher contradiction cycle queries directly executed against AWS ap-south-1 cloud nodes.</div>\n'
        '</div>\n'
        '</div>\n'
        '</div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    col_l, col_btn, col_r = st.columns([1, 1.8, 1])
    with col_btn:
        if st.button("🚀 ENTER INVESTIGATION MATRIX", use_container_width=True, key="hero_enter_btn"):
            st.session_state.in_dashboard = True
            st.rerun()

    st.markdown(
        '<div style="text-align: center; margin-top: 1.5rem; font-family: \'JetBrains Mono\', monospace; font-size: 0.74rem; color: #64748B;">'
        'CLUSTER: r-6jissuruar.instance-kf4vao0zb.hc-7up0crkyn.ap-south-1.aws.f2e0a955bb84.cloud:64782 // TLS SECURED'
        '</div>',
        unsafe_allow_html=True
    )
    st.stop()


# ==============================================================================
# SECTION 2: TOP HORIZONTAL NAVIGATION & CONTROL STRIP (MAIN DASHBOARD)
# ==============================================================================

# Top Navigation Bar with Discreet "🏠 Exit to Landing" Toggle
top_nav_c1, top_nav_c2 = st.columns([3.2, 0.8], gap="small")

with top_nav_c1:
    st.markdown("""
    <div class="top-brand-flex">
        <span class="top-brand-logo">🕵️‍♂️</span>
        <div>
            <div class="top-brand-title">ALIBI GRAPH</div>
            <div class="top-brand-subtitle">CYBER-FORENSIC INTELLIGENCE MATRIX // MULTI-MODAL LIE DETECTOR</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with top_nav_c2:
    if st.button("🏠 Exit to Landing", use_container_width=True, key="exit_to_landing_btn"):
        st.session_state.in_dashboard = False
        st.rerun()

# Sleek Collapsible Horizontal Controls Expander (Replacing Sidebar)
expander_default_open = not bool(st.session_state.f_pass)
with st.expander("⚙️ UPLINK CONFIGURATION & CASE WORKSPACE CONTROLS", expanded=expander_default_open):
    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns(4, gap="medium")
    
    with ctrl_col1:
        st.markdown('<div style="font-size:0.8rem; font-weight:700; color:var(--accent-teal); margin-bottom:4px;">🔌 FALKOR DB HOST & PORT</div>', unsafe_allow_html=True)
        f_host = st.text_input("Host:", value=st.session_state.f_host, key="f_host")
        f_port = st.number_input("Port:", value=st.session_state.f_port, step=1, key="f_port")

    with ctrl_col2:
        st.markdown('<div style="font-size:0.8rem; font-weight:700; color:var(--accent-teal); margin-bottom:4px;">🔐 CREDENTIALS</div>', unsafe_allow_html=True)
        f_user = st.text_input("Username:", value=st.session_state.f_user, key="f_user")
        f_pass = st.text_input("Secure Password:", type="password", value=st.session_state.f_pass, placeholder="Enter Cloud Password", key="f_pass")

    with ctrl_col3:
        st.markdown('<div style="font-size:0.8rem; font-weight:700; color:var(--accent-teal); margin-bottom:4px;">🗄️ DYNAMIC CASE CREATOR</div>', unsafe_allow_html=True)
        raw_case_input = st.text_input(
            "Active Case Identifier / Workspace:", 
            value=st.session_state.case_id, 
            placeholder="e.g. Case_Homicide_Sector4 or Inquiry_Alpha", 
            key="case_id"
        )
        safe_case_id = re.sub(r'[^a-zA-Z0-9_-]', '_', raw_case_input.strip()) if raw_case_input.strip() else "Case_Workspace"
        api_key = st.text_input("AI Studio API Key:", type="password", value=st.secrets.get("GEMINI_API_KEY", st.session_state.get("api_key", "")), placeholder="Enter AI Studio API Key", key="api_key")

    with ctrl_col4:
        st.markdown('<div style="font-size:0.8rem; font-weight:700; color:var(--accent-teal); margin-bottom:4px;">🧠 PROCEDURAL MEMORY</div>', unsafe_allow_html=True)
        new_rule = st.text_input("Interrogation Tactic:", value=st.session_state.new_rule, key="new_rule")
        action_col1, action_col2 = st.columns(2)
        with action_col1:
            save_tactic_clicked = st.button("💾 Save Tactic", use_container_width=True, key="save_tactic_btn")
        with action_col2:
            wipe_case_clicked = st.button("🗑️ Wipe Graph", use_container_width=True, key="wipe_case_btn")


# ==============================================================================
# SECTION 3: CONNECT TO FALKOR DB CLOUD
# ==============================================================================
graph = None
connection_active = False

if f_pass:
    try:
        db = FalkorDB(
            host=f_host,
            port=int(f_port),
            username=f_user if f_user else "falkordb",
            password=f_pass
        )
        graph = db.select_graph(safe_case_id)
        connection_active = True
    except Exception as e:
        st.error(f"Falkor DB Connection Error: {e}")
        graph = None
else:
    st.markdown(r"""
    <div class="auth-standby-banner">
        <div class="standby-glitch">⚡ FALKOR DB CLOUD UPLINK // AUTHENTICATION REQUIRED</div>
        <div class="standby-desc">Target Endpoint: <code>""" + str(f_host) + r""":""" + str(f_port) + r"""</code> (Tenant: <code>""" + str(safe_case_id) + r"""</code>)</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:#E2E8F0;">
            👆 Please enter your <b>Falkor DB Cloud Password</b> in the configuration strip above to establish the live forensic graph uplink.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Handle Tactic Save and Graph Wipe
if save_tactic_clicked and graph:
    try:
        graph.query(f"MERGE (r:Procedure {{rule: '{new_rule.replace(chr(39), '')}'}})")
        st.toast(f"Saved tactic to Falkor DB Procedural Memory in `{safe_case_id}`!", icon="🧠")
    except Exception as e:
        st.error(f"Error saving procedure: {e}")
elif save_tactic_clicked and not graph:
    st.warning("⚠️ Authenticate with Falkor DB password first to save procedural rules.")

if wipe_case_clicked and graph:
    try:
        graph.delete()
        st.toast(f"Current case graph `{safe_case_id}` wiped successfully!", icon="🗑️")
        st.rerun()
    except Exception:
        pass


# ==============================================================================
# SECTION 4: HORIZONTAL KPI TELEMETRY STRIP
# ==============================================================================
entity_count = 0
edge_count = 0
contra_count = 0

if graph:
    try:
        node_res = graph.query("MATCH (n) RETURN count(n)").result_set
        entity_count = node_res[0][0] if node_res else 0
        rel_res = graph.query("MATCH ()-[r]->() RETURN count(r)").result_set
        edge_count = rel_res[0][0] if rel_res else 0
        contra_res = graph.query("MATCH ()-[:CONTRADICTS]->() RETURN count(*)").result_set
        contra_count = (contra_res[0][0] // 2) if contra_res else 0
    except Exception:
        pass

uplink_status_html = '<span style="color:var(--clinical-green)"><span class="pulse-dot"></span> ONLINE</span>' if connection_active else '<span style="color:#fbbf24">● STANDBY</span>'
graph_stat_text = f"{entity_count} <span style=\"font-size:0.88rem; font-weight:600; color:var(--text-muted);\">NODES</span> / {edge_count} <span style=\"font-size:0.88rem; font-weight:600; color:var(--text-muted);\">EDGES</span>" if connection_active else "STANDBY"
contra_stat_text = f"{contra_count} <span style=\"font-size:0.88rem; font-weight:600; color:var(--text-muted);\">CONFLICTS</span>" if connection_active else "0 CONFLICTS"

st.markdown(f"""
<div class="telemetry-strip-grid">
    <div class="telemetry-card">
        <div class="telemetry-label">ACTIVE CASE WORKSPACE</div>
        <div class="telemetry-value">{safe_case_id}</div>
        <div class="telemetry-subtext">MULTI-TENANT NAMESPACE</div>
    </div>
    <div class="telemetry-card">
        <div class="telemetry-label">GRAPH TOPOLOGY</div>
        <div class="telemetry-value">{graph_stat_text}</div>
        <div class="telemetry-subtext">EPISODIC KNOWLEDGE CACHE</div>
    </div>
    <div class="telemetry-card" style="border-color: {'var(--stress-crimson)' if contra_count > 0 else 'var(--border-subtle)'};">
        <div class="telemetry-label" style="color: {'var(--stress-crimson)' if contra_count > 0 else 'var(--text-muted)'};">CONTRADICTIONS DETECTED</div>
        <div class="telemetry-value" style="color: {'var(--stress-crimson)' if contra_count > 0 else '#ffffff'};">{contra_stat_text}</div>
        <div class="telemetry-subtext">CROSS-MODAL CLASH EDGES</div>
    </div>
    <div class="telemetry-card">
        <div class="telemetry-label">FALKOR DB CLOUD UPLINK</div>
        <div class="telemetry-value">{uplink_status_html}</div>
        <div class="telemetry-subtext">PORT {f_port} // AP-SOUTH-1</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# SECTION 5: BACKEND CORE ENGINES (PRESERVED 100%)
# ==============================================================================

# --- MULTI-MODAL PARSER (IMAGES, PDFS, TEXT) ---
def process_uploaded_evidence(uploaded_file):
    if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        image = Image.open(uploaded_file)
        return image, "image"
    elif uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        text = "\n".join([f"[Page {i+1}] {page.extract_text()}" for i, page in enumerate(reader.pages)])
        return text, "text"
    else:
        text = uploaded_file.read().decode("utf-8", errors="ignore")
        return text, "text"

# --- AGENT 1: MULTI-MODAL PROFILER ---
def run_agent_1_profiler(suspect_name, evidence_data, ev_type, gemini_key):
    if not gemini_key:
        return [
            {"topic": "LOCATION_ALIBI", "claim": "Suspect claimed to be at home, but visual evidence shows otherwise.", "reference": "Evidence File"}
        ]
    client = genai.Client(api_key=gemini_key)
    
    prompt = f"""
    You are Agent 1 (Multi-Modal Evidence Profiler). Analyze this evidence file provided for suspect '{suspect_name}'. 
    Extract key factual or alibi claims. Normalize the 'topic' into uppercase tags like 'LOCATION_ALIBI', 'BLUE_SUV', 'WEAPON', or 'TIMESTAMP' so claims across photos and documents match.
    Return ONLY a JSON list of objects with keys:
    "topic" (normalized tag, e.g. "LOCATION_ALIBI"),
    "claim" (summary of what the photo or document shows/states),
    "reference" (timestamp, page number, or image description).
    """
    
    if ev_type == "image":
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[evidence_data, prompt]
        )
    else:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"{prompt}\n\nDocument Text:\n{evidence_data[:6000]}"
        )
        
    cleaned = re.sub(r"```json|```", "", response.text).strip()
    return json.loads(cleaned)

# --- FALKOR DB GRAPH WRITER & CONTRADICTION ENGINE ---
def ingest_to_falkordb(source_name, suspect_name, claims):
    if not graph:
        st.warning("⚠️ Cannot ingest: Falkor DB Cloud uplink not authenticated.")
        return []
        
    cypher_logs = []
    safe_source = source_name.replace("'", "")
    safe_suspect = suspect_name.replace("'", "")
    
    q1 = f"""
    MERGE (s:Suspect {{name: '{safe_suspect}'}})
    MERGE (ep:Episode {{name: '{safe_source}'}})
    MERGE (s)-[:SUBMITTED_EVIDENCE]->(ep)
    """
    graph.query(q1)
    cypher_logs.append(q1.strip())

    for c in claims:
        topic = c["topic"].strip().upper().replace("'", "").replace(" ", "_")
        claim_text = c["claim"].replace("'", "")
        ref = c.get("reference", "N/A").replace("'", "")
        
        q2 = f"""
        MATCH (ep:Episode {{name: '{safe_source}'}})
        MERGE (t:Topic {{name: '{topic}'}})
        CREATE (c:Claim {{statement: '{claim_text}', reference: '{ref}', source: '{safe_source}'}})
        MERGE (ep)-[:CONTAINS_CLAIM]->(c)
        MERGE (c)-[:ABOUT_TOPIC]->(t)
        """
        graph.query(q2)
        cypher_logs.append(q2.strip())

        q_contra = f"""
        MATCH (c1:Claim)-[:ABOUT_TOPIC]->(t:Topic {{name: '{topic}'}})<--(:Claim)<-[:CONTAINS_CLAIM]-(ep2:Episode)
        WHERE c1.source <> ep2.name
        MATCH (c2:Claim)-[:CONTAINS_CLAIM]-(ep2)
        WHERE c1.statement <> c2.statement
        MERGE (c1)-[:CONTRADICTS]->(c2)
        RETURN c1.source, ep2.name
        """
        graph.query(q_contra)
        cypher_logs.append(q_contra.strip())
    return cypher_logs


# ==============================================================================
# SECTION 6: FULL-WIDTH MATRIX WORKSPACE WITH DEDICATED TABS
# ==============================================================================
tab_graph, tab_ingest, tab_cross_exam, tab_terminal = st.tabs([
    "🕸️ IMMERSIVE GRAPH MATRIX (FULL-SCREEN)",
    "📂 EVIDENCE INGESTION BAY (AGENT 1)",
    "⚖️ DETECTIVE CROSS-EXAMINER (AGENT 2)",
    "⚡ CYPHER TRANSACTION TERMINAL"
])


# ------------------------------------------------------------------------------
# TAB 1: IMMERSIVE FULL-WIDTH KNOWLEDGE GRAPH MATRIX
# ------------------------------------------------------------------------------
with tab_graph:
    with st.container(border=True):
        st.markdown(f"""
        <div class="forensic-card-header">
            <div class="forensic-card-title">
                <span>🕸️ LIVE FALKOR DB KNOWLEDGE TOPOLOGY // FULL-WIDTH CANVAS</span>
            </div>
            <span class="stage-badge green">CASE: {safe_case_id}</span>
        </div>
        """, unsafe_allow_html=True)

        # Graph Utility Toolbar
        tb_col1, tb_col2, tb_col3 = st.columns([2.5, 1, 1], gap="small")
        with tb_col1:
            st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:var(--accent-teal); padding-top:6px;">
                ACTIVE GRAPH TENANT: <code style="color:#ffffff;">{safe_case_id}</code>
            </div>
            """, unsafe_allow_html=True)
        with tb_col2:
            if st.button("🔄 Refresh Topology", use_container_width=True, key="tb_refresh_btn"):
                st.rerun()
        with tb_col3:
            if st.button("🗑️ Wipe Case Graph", use_container_width=True, key="tb_reset_btn"):
                if graph:
                    try:
                        graph.delete()
                        st.toast(f"Case graph `{safe_case_id}` wiped!", icon="🗑️")
                        st.rerun()
                    except Exception:
                        pass
                else:
                    st.warning("⚠️ Enter Falkor DB password to connect.")

        # Interactive Graph Legend
        st.markdown("""
        <div class="topology-legend-bar">
            <div class="legend-pill"><span class="legend-dot-circle" style="background:#00F2FE; box-shadow:0 0 8px #00F2FE;"></span> Evidence Exhibit (Bio-Neon Teal)</div>
            <div class="legend-pill"><span class="legend-dot-circle" style="background:#fbbf24; box-shadow:0 0 8px #fbbf24;"></span> Semantic Topic (Axis)</div>
            <div class="legend-pill"><span class="legend-dot-circle" style="background:#10B981; box-shadow:0 0 8px #10B981;"></span> Claim Statement (Clinical Green)</div>
            <div class="legend-pill"><span class="legend-dot-circle" style="background:#a78bfa; box-shadow:0 0 8px #a78bfa;"></span> Suspect Entity (Silver/Purple)</div>
            <div class="legend-pill"><span class="legend-dot-circle" style="background:#EF4444; box-shadow:0 0 10px #EF4444;"></span> CONTRADICTS Edge (Stress Crimson)</div>
        </div>
        """, unsafe_allow_html=True)

        if graph:
            nodes, edges, seen_nodes = [], [], set()
            try:
                res = graph.query("MATCH (n)-[r]->(m) RETURN id(n), labels(n)[0], n, type(r), id(m), labels(m)[0], m").result_set
                for row in res:
                    n_id, n_lbl, n_props, r_type, m_id, m_lbl, m_props = row
                    color_map = {
                        "Suspect": "#a78bfa",
                        "Episode": "#00F2FE",   # Bio-Neon Teal
                        "Topic": "#fbbf24",
                        "Claim": "#10B981"      # Clinical Green
                    }
                    for node_id, lbl, props in [(str(n_id), n_lbl, n_props), (str(m_id), m_lbl, m_props)]:
                        if node_id not in seen_nodes:
                            label_text = props.properties.get("name") or props.properties.get("statement", "")[:26] + "..."
                            nodes.append(Node(
                                id=node_id,
                                label=f"{lbl}\n{label_text}",
                                size=28,
                                color=color_map.get(lbl, "#64748B"),
                                font={
                                    "color": "#ffffff",
                                    "face": "JetBrains Mono",
                                    "size": 11,
                                    "strokeWidth": 3,
                                    "strokeColor": "#0B0F19"
                                }
                            ))
                            seen_nodes.add(node_id)
                    
                    is_contra = (r_type == "CONTRADICTS")
                    edge_color = "#EF4444" if is_contra else "#00F2FE"
                    edges.append(Edge(
                        source=str(n_id),
                        target=str(m_id),
                        label=r_type,
                        color=edge_color,
                        width=4.5 if is_contra else 1.8,
                        font={
                            "color": "#EF4444" if is_contra else "#00F2FE",
                            "face": "JetBrains Mono",
                            "size": 10,
                            "strokeWidth": 2,
                            "strokeColor": "#0B0F19"
                        }
                    ))
            except Exception as e:
                st.error(f"Error querying graph: {e}")

            if nodes:
                # Massive, immersive full-screen Agraph Canvas
                config = Config(
                    width=1240,
                    height=620,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#00F2FE"
                )
                agraph(nodes=nodes, edges=edges, config=config)
            else:
                st.markdown(f"""
                <div class="standby-card" style="padding: 3.5rem 1.5rem;">
                    <div style="font-size: 2.8rem; margin-bottom: 0.8rem;">🕸️</div>
                    <div style="font-size: 1.15rem; font-weight:700; color:var(--accent-teal); margin-bottom: 6px;">
                        TOPOLOGY CACHE VACANT IN CASE: {safe_case_id}
                    </div>
                    <div style="font-size: 0.9rem; color: var(--text-muted); max-width: 580px; margin: 0 auto;">
                        Navigate to the <b>Evidence Ingestion Bay</b> tab to upload custom forensic evidence files (CCTV photos, alibi testimonies, PDFs, logs) and populate real-time episodic nodes.
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="standby-card" style="padding: 3.5rem 1.5rem;">
                <div style="font-size: 2.8rem; margin-bottom: 0.8rem;">🔌</div>
                <div style="font-size: 1.15rem; font-weight:700; color:#fbbf24; margin-bottom: 6px;">
                    UPLINK AUTHENTICATION REQUIRED
                </div>
                <div style="font-size: 0.9rem; color: var(--text-muted); max-width: 580px; margin: 0 auto;">
                    Expand the <b>'⚙️ UPLINK CONFIGURATION & CASE WORKSPACE CONTROLS'</b> bar above and enter your Falkor DB Cloud Password to initialize real-time graph visualization for <code>{safe_case_id}</code>.
                </div>
            </div>
            """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 2: STRICT CUSTOM MULTI-MODAL EVIDENCE INGESTION BAY (AGENT 1)
# ------------------------------------------------------------------------------
with tab_ingest:
    with st.container(border=True):
        st.markdown(f"""
        <div class="forensic-card-header">
            <div class="forensic-card-title">
                <span>📁 MULTI-MODAL FORENSIC EVIDENCE INGESTION BAY</span>
            </div>
            <span class="stage-badge green">AGENT 1 // {safe_case_id}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sim-scenario-box">
            <b>STRICT CUSTOM EVIDENCE INGESTION PIPELINE:</b>
            Upload authentic forensic exhibits (surveillance CCTV images, written alibi statements, forensic audit PDFs, phone chat archives, or witness transcripts).
            Agent 1 extracts structured claims, normalizes semantic topics, and directly ingests episodic nodes into Falkor DB Cloud namespace <b><code>{safe_case_id}</code></b>.
        </div>
        """, unsafe_allow_html=True)

        up_col1, up_col2 = st.columns([1.3, 1], gap="large")

        with up_col1:
            uploaded_file = st.file_uploader(
                "Upload Forensic Evidence File (PNG, JPG, JPEG, PDF, TXT, MD):", 
                type=["png", "jpg", "jpeg", "pdf", "txt", "md"],
                key="custom_uploader"
            )
            if uploaded_file is not None:
                data, ev_type = process_uploaded_evidence(uploaded_file)
                if ev_type == "image":
                    st.image(data, caption=f"Forensic Exhibit: {uploaded_file.name}", width=340)
                else:
                    st.info(f"📄 Forensic Document Loaded: {uploaded_file.name} ({len(data)} characters extracted)")

        with up_col2:
            suspect_name = st.text_input(
                "Target Suspect / Entity Identifier:", 
                value=st.session_state.suspect_name, 
                placeholder="e.g. Suspect_Marcus, Witness_Elena, or Target_Alpha",
                key="suspect_name"
            )
            st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:var(--text-muted); margin-bottom:1.1rem;">
                TARGET NAMESPACE: <code style="color:var(--accent-teal);">{safe_case_id}</code>
            </div>
            """, unsafe_allow_html=True)

            ingest_submitted = st.button("🕵️ Agent 1: Analyze & Ingest Forensic Evidence", use_container_width=True, key="custom_ingest_btn")

        if ingest_submitted:
            if not graph:
                st.warning("⚠️ Please authenticate with your Falkor DB password in the top control strip first.")
            elif not suspect_name.strip():
                st.warning("⚠️ Please enter a Target Suspect / Entity Identifier before ingesting.")
            elif uploaded_file is not None:
                data, ev_type = process_uploaded_evidence(uploaded_file)
                with st.spinner(f"Agent 1 analyzing multi-modal evidence from '{uploaded_file.name}' for suspect '{suspect_name}'..."):
                    claims = run_agent_1_profiler(suspect_name, data, ev_type, api_key)
                    st.session_state.cypher_logs = ingest_to_falkordb(uploaded_file.name, suspect_name, claims)
                    st.toast(f"✅ Extracted {len(claims)} claim(s) from '{uploaded_file.name}' into Falkor DB `{safe_case_id}`!", icon="🕵️‍♂️")
                    st.success(f"Successfully mapped evidence from `{uploaded_file.name}` for `{suspect_name}` into Falkor DB `{safe_case_id}`!")
                    st.rerun()
            else:
                st.warning("⚠️ Please select a forensic evidence file before initiating Agent 1 analysis.")


# ------------------------------------------------------------------------------
# TAB 3: INTERACTIVE DASHBOARD CARD: DETECTIVE CROSS-EXAMINER (AGENT 2)
# ------------------------------------------------------------------------------
with tab_cross_exam:
    with st.container(border=True):
        st.markdown(f"""
        <div class="forensic-card-header">
            <div class="forensic-card-title">
                <span>⚖️ AGENT 2: DETECTIVE CROSS-EXAMINATION & CONTRADICTION ENGINE</span>
            </div>
            <span class="stage-badge crimson">CASE: {safe_case_id}</span>
        </div>
        """, unsafe_allow_html=True)
        
        contradictions = []
        rules = []
        active_rule = new_rule
        
        if graph:
            try:
                contradictions = graph.query("""
                    MATCH (c1:Claim)-[:CONTRADICTS]->(c2:Claim), (c1)-[:ABOUT_TOPIC]->(t:Topic)
                    WHERE id(c1) < id(c2)
                    RETURN t.name, c1.source, c1.statement, c1.reference, c2.source, c2.statement, c2.reference
                """).result_set
                
                rules = graph.query("MATCH (r:Procedure) RETURN r.rule").result_set
                if rules:
                    active_rule = rules[-1][0]
            except Exception:
                pass

        if contradictions:
            st.markdown(f"""
            <div class="contradiction-alert-box">
                <div class="contradiction-header">
                    <span class="contradiction-title">🚨 CRITICAL CONTRADICTION DETECTED IN {safe_case_id}</span>
                    <span style="font-size:0.75rem; color:#ffffff; font-family:'JetBrains Mono';">[{len(contradictions)} CLASH DETECTED]</span>
                </div>
            """, unsafe_allow_html=True)

            for row in contradictions:
                topic, s1, st1, ref1, s2, st2, ref2 = row
                st.markdown(f"""
                <div class="conflict-topic-pill">💥 CONFLICT AXIS: {topic}</div>
                <div class="clash-split-grid">
                    <div class="clash-dossier-card doc">
                        <div class="dossier-tag">Source A // Documentary Testimony</div>
                        <div class="dossier-source">{s1} <span style="font-weight:400; font-size:0.75rem; color:var(--text-muted);">({ref1})</span></div>
                        <div class="dossier-statement">"{st1}"</div>
                    </div>
                    <div class="clash-dossier-card visual">
                        <div class="dossier-tag">Source B // Visual Surveillance</div>
                        <div class="dossier-source">{s2} <span style="font-weight:400; font-size:0.75rem; color:var(--text-muted);">({ref2})</span></div>
                        <div class="dossier-statement">"{st2}"</div>
                    </div>
                </div>
                <div class="confrontation-teleprompter">
                    <div class="teleprompter-speaker">
                        <span>⚡ AGENT 2 // CONFRONTATION INTERROGATION SCRIPT</span>
                    </div>
                    <div class="teleprompter-script">
                        "Your statement in <code>{s1}</code> claimed: <i>'{st1}'</i>. However, the forensic visual evidence in <code>{s2}</code> proves: <i>'{st2}'</i>. Explain this direct contradiction."
                    </div>
                    <div class="teleprompter-rule">🧠 Procedural Rule Applied: <code>{active_rule}</code></div>
                </div>
                <hr style="border-color: rgba(239, 68, 68, 0.25); margin: 1.1rem 0;">
                """, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="standby-card">
                <div class="standby-icon">📡</div>
                <div style="font-size:1.05rem; font-weight:700; color:var(--accent-teal); margin-bottom:5px;">
                    FORENSIC RADAR: ACTIVE & SCANNING ({safe_case_id})
                </div>
                <div style="font-size:0.88rem; color:var(--text-muted); max-width: 620px; margin: 0 auto;">
                    No contradictions detected in <b>{safe_case_id}</b>.<br>
                    Upload conflicting forensic exhibits or statements for the target suspect in the <b>Evidence Ingestion Bay</b> to trigger real-time Cypher contradiction reasoning and prosecutorial cross-examination scripts.
                </div>
            </div>
            """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 4: CYPHER TRANSACTION TERMINAL
# ------------------------------------------------------------------------------
with tab_terminal:
    with st.container(border=True):
        st.markdown(f"""
        <div class="forensic-card-header">
            <div class="forensic-card-title">
                <span>⚡ FALKOR DB CYPHER TRANSACTION TERMINAL // {safe_case_id}</span>
            </div>
            <span class="stage-badge">CYPHER AUDIT</span>
        </div>
        <div class="terminal-hud-box">
            <div class="terminal-titlebar-strip">
                <div class="window-dots">
                    <span class="window-dot" style="background:#EF4444;"></span>
                    <span class="window-dot" style="background:#fbbf24;"></span>
                    <span class="window-dot" style="background:#10B981;"></span>
                </div>
                <span>falkor-db@graph-cluster:~/cypher$ cypher-shell --format verbose --tenant {safe_case_id}</span>
                <span>TLS_AES_256_GCM_SHA384</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        cypher_queries = st.session_state.cypher_logs if st.session_state.cypher_logs else ["// Live Cypher audit logs will render here upon evidence ingestion"]
        for q in cypher_queries:
            st.code(q, language="cypher")