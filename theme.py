"""CrimeWatch — Forensic Noir Theme."""
import streamlit as st

PALETTE = {
    "bg_main": "#0A0A0F",
    "bg_card": "#151519",
    "bg_card_light": "#1F1F26",
    "accent_crimson": "#DC2626",
    "accent_blood": "#991B1B",
    "accent_amber": "#F59E0B",
    "accent_yellow": "#FBBF24",
    "accent_white": "#F5F5F4",
    "accent_green": "#10B981",
    "text_primary": "#F5F5F4",
    "text_secondary": "#A8A29E",
    "text_muted": "#57534E",
    "border": "#27272A",
}

CHART_COLORS = ["#DC2626", "#F59E0B", "#FBBF24", "#EAB308", "#A16207",
                "#991B1B", "#7F1D1D", "#450A0A", "#78716C", "#44403C"]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="#151519",
    plot_bgcolor="#151519",
    font=dict(family="Inter", color="#F5F5F4", size=12),
    title_font=dict(family="Oswald", size=17, color="#F5F5F4"),
    colorway=CHART_COLORS,
    xaxis=dict(gridcolor="#27272A", linecolor="#3F3F46", zerolinecolor="#27272A"),
    yaxis=dict(gridcolor="#27272A", linecolor="#3F3F46", zerolinecolor="#27272A"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    margin=dict(t=50, b=40, l=40, r=20),
    hoverlabel=dict(bgcolor="#1F1F26", font_family="Inter", font_color="white"),
)


def apply_theme(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig


def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@700;900&display=swap');

:root {
    --bg-main: #0A0A0F;
    --bg-card: #151519;
    --bg-card-light: #1F1F26;
    --accent-crimson: #DC2626;
    --accent-blood: #991B1B;
    --accent-amber: #F59E0B;
    --accent-yellow: #FBBF24;
    --accent-white: #F5F5F4;
    --accent-green: #10B981;
    --text-primary: #F5F5F4;
    --text-secondary: #A8A29E;
    --text-muted: #57534E;
    --border: #27272A;
}

html, body, [class*="css"] {
    background: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(at 15% 10%, rgba(220, 38, 38, 0.06) 0%, transparent 50%),
        radial-gradient(at 85% 90%, rgba(245, 158, 11, 0.04) 0%, transparent 50%),
        linear-gradient(135deg, #0A0A0F 0%, #110D10 100%) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0A0F 0%, #151519 100%) !important;
    border-right: 1px solid var(--accent-crimson) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* === HERO === */
.hero-wrapper { position: relative; padding: 20px 0 12px 0; }
.hero {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 4.8rem;
    letter-spacing: -0.02em;
    background: linear-gradient(180deg, #F5F5F4 0%, #DC2626 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin: 0;
    text-shadow: 0 0 40px rgba(220, 38, 38, 0.15);
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--accent-crimson);
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 8px;
    font-weight: 700;
}
.hero-divider {
    height: 1px;
    background: linear-gradient(to right, #DC2626, #991B1B, transparent);
    margin: 16px 0 22px 0;
}

/* === CLASSIFIED STRIP (like case file header) === */
.classified-strip {
    background: repeating-linear-gradient(45deg, #DC2626, #DC2626 10px, #991B1B 10px, #991B1B 20px);
    color: white;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.35em;
    padding: 6px 20px;
    text-align: center;
    font-weight: 700;
    margin-bottom: 16px;
    border-radius: 3px;
}

/* === SECTION === */
.sec-hdr {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 1.5rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-left: 4px solid var(--accent-crimson);
    padding-left: 14px;
    margin: 28px 0 14px 0;
    color: var(--text-primary);
}
.sec-hdr-amber { border-left-color: var(--accent-amber) !important; }
.sec-hdr-blood { border-left-color: var(--accent-blood) !important; }
.sec-hdr-green { border-left-color: var(--accent-green) !important; }

/* === KPI CARD (evidence card style) === */
.kpi-card {
    background: linear-gradient(135deg, #151519 0%, #1F1F26 100%);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 18px 22px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
    height: 100%;
}
.kpi-card:hover {
    border-color: var(--accent-crimson);
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(220, 38, 38, 0.2);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; bottom: 0;
    width: 3px;
    background: var(--kpi-accent, var(--accent-crimson));
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 60px; height: 60px;
    background: radial-gradient(circle at top right, var(--kpi-accent, var(--accent-crimson)) 0%, transparent 70%);
    opacity: 0.08;
}
.kpi-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: var(--text-secondary);
    text-transform: uppercase;
    margin-bottom: 6px;
    font-weight: 700;
}
.kpi-value {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 2.6rem;
    line-height: 1;
    color: var(--text-primary);
}
.kpi-delta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    margin-top: 6px;
    letter-spacing: 0.08em;
}
.kpi-icon {
    position: absolute;
    right: 16px; top: 50%;
    transform: translateY(-50%);
    font-size: 2.2rem;
    opacity: 0.15;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card);
    border-radius: 4px;
    padding: 4px;
    gap: 3px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    color: var(--text-secondary);
    height: 42px;
    padding: 0 20px;
    border-radius: 3px;
    transition: all 0.3s;
    text-transform: uppercase;
    font-weight: 700;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(220, 38, 38, 0.1);
    color: var(--text-primary);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #DC2626, #991B1B) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
}

/* === WIDGETS === */
div[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
}
.stSelectbox label, .stSlider label, .stMultiSelect label, .stRadio label,
.stTextInput label, .stTextArea label, .stNumberInput label, .stFileUploader label,
.stCheckbox label {
    color: var(--text-secondary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
input, textarea {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border-color: var(--border) !important;
    font-family: 'Inter', sans-serif !important;
}

/* === BUTTONS === */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #DC2626, #991B1B) !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    padding: 10px 20px !important;
    transition: all 0.3s !important;
    font-weight: 700 !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(220, 38, 38, 0.4);
}

/* === INFO BOX === */
.info-box {
    background: linear-gradient(135deg, rgba(220, 38, 38, 0.1), rgba(153, 27, 27, 0.03));
    border-left: 3px solid var(--accent-crimson);
    padding: 12px 18px;
    border-radius: 3px;
    margin: 10px 0;
    font-family: 'Inter', sans-serif;
    font-size: 0.86rem;
    color: var(--text-secondary);
}
.warning-box {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.03));
    border-left: 3px solid var(--accent-amber);
    padding: 12px 18px;
    border-radius: 3px;
    margin: 10px 0;
    color: var(--text-secondary);
}

/* === BADGES (severity tags) === */
.badge {
    display: inline-block;
    background: linear-gradient(135deg, #DC2626, #991B1B);
    color: white !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    padding: 4px 10px;
    border-radius: 3px;
    margin-right: 5px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 700;
}
.badge-amber { background: linear-gradient(135deg, #F59E0B, #B45309) !important; }
.badge-green { background: linear-gradient(135deg, #10B981, #047857) !important; }
.badge-gray  { background: linear-gradient(135deg, #57534E, #292524) !important; }

/* === CASE CARD (like a case file) === */
.case-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 14px 18px;
    margin: 8px 0;
    border-left: 3px solid var(--accent-crimson);
    transition: all 0.25s;
    position: relative;
    font-family: 'Inter', sans-serif;
}
.case-card:hover {
    background: var(--bg-card-light);
    transform: translateX(4px);
    border-left-width: 5px;
    box-shadow: 0 6px 20px rgba(220, 38, 38, 0.15);
}
.case-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: var(--text-muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.case-headline {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-primary);
    margin: 4px 0;
}
.case-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    color: var(--text-secondary);
    letter-spacing: 0.08em;
}

/* === FEATURE TILES === */
.feature-tile {
    background: linear-gradient(135deg, #151519 0%, #1F1F26 100%);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 22px;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
    height: 100%;
}
.feature-tile:hover {
    border-color: var(--accent-crimson);
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(220, 38, 38, 0.18);
}
.feature-icon {
    font-size: 2.4rem;
    margin-bottom: 10px;
    display: block;
    filter: grayscale(30%);
}
.feature-title {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 1.3rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-primary);
    margin-bottom: 6px;
}
.feature-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* === DATA TABLES === */
[data-testid="stDataFrame"] {
    background: var(--bg-card) !important;
    border-radius: 4px;
    border: 1px solid var(--border);
}

/* === METRICS === */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 12px 16px;
}

/* === EXPANDER === */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 0.1em !important;
}

/* === SLIDER === */
.stSlider [data-baseweb="slider"] > div > div > div {
    background: linear-gradient(90deg, #DC2626, #F59E0B) !important;
}

/* === CLEAN CHROME === */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
}
.block-container { padding-top: 2rem !important; max-width: 1500px; }

/* === ANIMATIONS === */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeInUp 0.5s ease-out; }

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.blink-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent-crimson);
    box-shadow: 0 0 12px var(--accent-crimson);
    animation: blink 1.5s infinite;
    margin-right: 8px;
    vertical-align: middle;
}

/* === STAMP (classified-style) === */
.stamp {
    display: inline-block;
    border: 2px solid var(--accent-crimson);
    color: var(--accent-crimson);
    padding: 4px 12px;
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    transform: rotate(-3deg);
    border-radius: 2px;
    background: rgba(220, 38, 38, 0.08);
}

/* === STAT STRIP === */
.stat-strip {
    display: flex;
    justify-content: space-around;
    padding: 14px;
    background: var(--bg-card);
    border-radius: 4px;
    border: 1px solid var(--border);
    border-top: 2px solid var(--accent-crimson);
    margin: 10px 0;
}
.stat-item { text-align: center; }
.stat-value {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 1.8rem;
    color: var(--accent-crimson);
    line-height: 1;
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: var(--text-muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 4px;
    font-weight: 700;
}

/* === CHAT BUBBLES === */
.chat-bubble {
    padding: 12px 18px;
    border-radius: 6px;
    margin: 8px 0;
    max-width: 82%;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    line-height: 1.55;
}
.chat-user {
    background: linear-gradient(135deg, #DC2626, #991B1B);
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 2px;
}
.chat-ai {
    background: #1F1F26;
    color: #F5F5F4;
    border: 1px solid #27272A;
    border-left: 3px solid var(--accent-amber);
    border-bottom-left-radius: 2px;
}
</style>
""", unsafe_allow_html=True)


def kpi_card(col, label, value, icon, color, delta=""):
    delta_html = f"<div class='kpi-delta' style='color:{color}'>{delta}</div>" if delta else ""
    col.markdown(
        f"<div class='kpi-card' style='--kpi-accent:{color}'>"
        f"<div class='kpi-label'>{label}</div>"
        f"<div class='kpi-value'>{value}</div>"
        f"{delta_html}<div class='kpi-icon'>{icon}</div></div>",
        unsafe_allow_html=True
    )


def section(title, accent="crimson"):
    cls = f"sec-hdr sec-hdr-{accent}" if accent != "crimson" else "sec-hdr"
    st.markdown(f'<div class="{cls}">{title}</div>', unsafe_allow_html=True)
