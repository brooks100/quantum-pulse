import streamlit as st
import yfinance as yf
import pandas as pd

# ──────────────────────────────────────────────
st.set_page_config(
    page_title="QUANTUM PULSE | Market Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ──────────────────────────────────────────────
# NEON HEADER + PROFESSIONAL BODY
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Orbitron:wght@500;700;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.mono { font-family: 'JetBrains Mono', monospace; }

html, body, .stApp, .block-container {
    background: #0a0a0f;
    color: #e8e8f0;
}

.block-container {
    padding-top: 0.5rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #3a3a4a; }

/* ══════════════════════════════
   NEON HEADER ANIMATIONS
   ══════════════════════════════ */

@keyframes neon-flicker {
    0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
        text-shadow:
            0 0 4px #fff,
            0 0 11px #fff,
            0 0 19px #fff,
            0 0 40px #00f0ff,
            0 0 80px #00f0ff,
            0 0 90px #00f0ff,
            0 0 100px #00f0ff,
            0 0 150px #00f0ff;
    }
    20%, 24%, 55% {
        text-shadow: none;
    }
}

@keyframes neon-pulse-cyan {
    0%, 100% {
        text-shadow: 0 0 5px #00f0ff, 0 0 15px #00f0ff, 0 0 30px #00f0ff, 0 0 60px #00f0ff;
    }
    50% {
        text-shadow: 0 0 10px #00f0ff, 0 0 25px #00f0ff, 0 0 50px #00f0ff, 0 0 100px #00f0ff, 0 0 140px #00f0ff;
    }
}

@keyframes icon-pulse {
    0%, 100% {
        filter: drop-shadow(0 0 8px #00f0ff) drop-shadow(0 0 20px #00f0ff);
        transform: scale(1);
    }
    50% {
        filter: drop-shadow(0 0 15px #ff00aa) drop-shadow(0 0 40px #ff00aa);
        transform: scale(1.12);
    }
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes scan-line {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

@keyframes blink {
    0%, 49% { opacity: 1; }
    50%, 100% { opacity: 0.2; }
}

@keyframes border-glow {
    0%, 100% { box-shadow: 0 0 5px rgba(0,240,255,0.3), inset 0 0 5px rgba(0,240,255,0.1); }
    50% { box-shadow: 0 0 20px rgba(255,0,170,0.5), inset 0 0 15px rgba(255,0,170,0.15); }
}

/* HERO */
.hero {
    text-align: center;
    padding: 3rem 0 2.5rem 0;
    position: relative;
    overflow: hidden;
    border-radius: 20px;
    margin-bottom: 1rem;
    animation: border-glow 3s ease-in-out infinite;
    background: radial-gradient(ellipse at center, rgba(0,240,255,0.05) 0%, transparent 70%);
}

.hero-icon {
    font-size: 3.5rem;
    margin-bottom: 0.5rem;
    display: inline-block;
    animation: icon-pulse 1.8s ease-in-out infinite;
}

.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(2rem, 6vw, 3.5rem);
    font-weight: 900;
    letter-spacing: 0.15em;
    margin: 0;
    line-height: 1.1;
    background: linear-gradient(90deg, #00f0ff, #ff00aa, #7c3aed, #00f0ff);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient-shift 4s ease infinite, neon-flicker 5s linear infinite;
}

.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #00f0ff;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    margin-top: 1rem;
    font-weight: 500;
    animation: neon-pulse-cyan 2s ease-in-out infinite;
}

.hero-sub .dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    background: #00ff88;
    border-radius: 50%;
    margin: 0 10px;
    vertical-align: middle;
    animation: blink 1s step-end infinite;
    box-shadow: 0 0 8px #00ff88;
}

/* Animated line under header */
.hero-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #00f0ff, #ff00aa, transparent);
    margin: 1.5rem auto 0 auto;
    width: 80%;
    position: relative;
    overflow: hidden;
    border-radius: 2px;
}
.hero-line::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 40%;
    height: 100%;
    background: linear-gradient(90deg, transparent, #ffffff, transparent);
    animation: scan-line 2s linear infinite;
}

/* ── STATS BAR ── */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    padding: 1.2rem 0;
    margin: 1rem 0;
    flex-wrap: wrap;
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: #00f0ff;
    text-shadow: 0 0 10px rgba(0,240,255,0.5);
}
.stat-label {
    font-size: 0.7rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}

.section-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin: 2rem 0 1.2rem 0;
    text-align: center;
}

/* ── CATEGORY CARDS ── */
.cat-card {
    background: linear-gradient(145deg, #14141c, #0f0f16);
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 1.3rem 1rem;
    text-align: center;
    transition: all 0.25s ease;
    margin-bottom: 0.8rem;
}
.cat-card:hover {
    border-color: #00f0ff;
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,240,255,0.2);
}
.cat-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.cat-name {
    font-size: 0.85rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 0.2rem;
}
.cat-count {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #475569;
}

/* ── CENTERED SCAN BUTTONS ── */
.stButton {
    text-align: center !important;
    width: 100%;
}
.stButton > button {
    background: linear-gradient(135deg, #00f0ff, #7c3aed);
    color: #fff;
    border: none;
    border-radius: 20px;
    padding: 0.45rem 1.8rem;
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    width: auto !important;
    display: inline-block !important;
    transition: all 0.2s ease;
    box-shadow: 0 0 15px rgba(0,240,255,0.3);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 25px rgba(0,240,255,0.6);
}

/* ── SIGNAL BADGES ── */
@keyframes pulse-green {
    0%,100% { box-shadow: 0 0 0 0 rgba(16,185,129,0.4); }
    50% { box-shadow: 0 0 0 6px rgba(16,185,129,0); }
}
@keyframes pulse-red {
    0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.4); }
    50% { box-shadow: 0 0 0 6px rgba(239,68,68,0); }
}
@keyframes pulse-yellow {
    0%,100% { box-shadow: 0 0 0 0 rgba(234,179,8,0.4); }
    50% { box-shadow: 0 0 0 6px rgba(234,179,8,0); }
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.badge-long {
    background: rgba(16,185,129,0.12);
    color: #34d399;
    border: 1px solid rgba(16,185,129,0.3);
    animation: pulse-green 2s infinite;
}
.badge-short {
    background: rgba(239,68,68,0.12);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.3);
    animation: pulse-red 2s infinite;
}
.badge-hold {
    background: rgba(234,179,8,0.12);
    color: #fbbf24;
    border: 1px solid rgba(234,179,8,0.3);
    animation: pulse-yellow 2s infinite;
}

/* ── RESULTS TABLE ── */
.results-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-size: 0.85rem;
}
.results-table th {
    background: #14141c;
    color: #00f0ff;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.8rem 1rem;
    text-align: left;
    border-bottom: 1px solid #1e1e2e;
    font-weight: 600;
}
.results-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #16161f;
    color: #cbd5e1;
}
.results-table tr:hover { background: rgba(0,240,255,0.05); }
.results-table .ticker {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    color: #f1f5f9;
}
.results-table .pos { color: #34d399; font-weight: 600; }
.results-table .neg { color: #f87171; font-weight: 600; }

.summary-card {
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}
.summary-long {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
}
.summary-short {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
}
.summary-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}

hr { border-color: #1e1e2e !important; margin: 2rem 0 !important; }

.footer {
    text-align: center;
    padding: 2rem 0 1rem 0;
    color: #475569;
    font-size: 0.75rem;
    border-top: 1px solid #16161f;
    margin-top: 3rem;
}

@media (max-width: 768px) {
    .stats-bar { gap: 1.5rem; }
    .stat-num { font-size: 1.2rem; }
    .results-table { font-size: 0.75rem; }
    .results-table th, .results-table td { padding: 0.5rem 0.6rem; }
}

#MainMenu, footer, [data-testid="stSidebar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# PULSE SOUND
# ──────────────────────────────────────────────
AUDIO_HTML = """
<audio id="pulseAudio" preload="auto">
  <source src="data:audio/wav;base64,UklGRiIAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQ4AAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIqK/7dKtQAA////////8PDw8PDw8PDw8PDw9fX19fX19fX19fX1/f39/f39/f39/f39/gICAICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA=" type="audio/wav">
<script>
const audioEl = document.getElementById('pulseAudio');
function playPulse() {
    if (audioEl) { audioEl.currentTime = 0; audioEl.volume = 0.4; audioEl.play().catch(() => {}); }
}
</script>
"""
st.components.v1.html(AUDIO_HTML, height=0)

def play_pulse_sound():
    st.markdown("<script>playPulse();</script>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SCAN FUNCTION
# ──────────────────────────────────────────────
def get_signal(full_name, ticker):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="3mo")
        if hist.empty or len(hist) < 5:
            return None
        price = round(hist.iloc[-1]['Close'], 2)
        chg_1w = round(((price - hist.iloc[-5]['Close']) / hist.iloc[-5]['Close']) * 100, 2)
        chg_1m = round(((price - hist.iloc[0]['Close']) / hist.iloc[0]['Close']) * 100, 2)
        ma20 = hist['Close'].tail(20).mean()
        above_ma = price > ma20
        recent_high = hist['High'].tail(10).max()
        dd = round(((price - recent_high) / recent_high) * 100, 2)

        if above_ma and chg_1w > 0 and chg_1m > 0:
            signal = "LONG"
            display_signal = "<span class='badge badge-long'>▲ LONG</span>"
        elif (not above_ma) or (chg_1w < -3) or (dd < -8):
            signal = "SHORT"
            display_signal = "<span class='badge badge-short'>▼ SHORT</span>"
        else:
            signal = "HOLD"
            display_signal = "<span class='badge badge-hold'>◆ HOLD</span>"

        return {
            "Asset": full_name,
            "Price": price,
            "1W %": chg_1w,
            "1M %": chg_1m,
            "Signal": display_signal,
            "_signal_raw": signal,
            "Drawdown %": dd
        }
    except Exception:
        return None

def color_pct(val):
    if val > 0: return f"<span class='pos'>+{val}%</span>"
    elif val < 0: return f"<span class='neg'>{val}%</span>"
    else: return f"<span>{val}%</span>"

def render_table(df):
    rows_html = ""
    for _, r in df.iterrows():
        rows_html += f"""
        <tr>
            <td class='ticker'>{r['Asset']}</td>
            <td class='mono'>{r['Price']}</td>
            <td>{color_pct(r['1W %'])}</td>
            <td>{color_pct(r['1M %'])}</td>
            <td>{r['Signal']}</td>
            <td>{color_pct(r['Drawdown %'])}</td>
        </tr>"""
    return f"""
    <table class='results-table'>
        <thead><tr><th>Instrument</th><th>Price</th><th>1W</th><th>1M</th><th>Signal</th><th>Drawdown</th></tr></thead>
        <tbody>{rows_html}</tbody>
    </table>"""

# ──────────────────────────────────────────────
# CATEGORIES with FULL NAMES
# ──────────────────────────────────────────────
CATEGORIES = [
    {"icon": "₿", "name": "Cryptocurrency", "assets": [
        ("Bitcoin", "BTC-USD"),
        ("Ethereum", "ETH-USD"),
        ("Solana", "SOL-USD"),
        ("Ripple", "XRP-USD"),
        ("Cardano", "ADA-USD"),
        ("Dogecoin", "DOGE-USD"),
        ("Avalanche", "AVAX-USD"),
        ("Polkadot", "DOT-USD"),
        ("Chainlink", "LINK-USD"),
        ("Uniswap", "UNI-USD"),
        ("Cosmos", "ATOM-USD"),
        ("Near Protocol", "NEAR-USD"),
        ("Arbitrum", "ARB-USD")
    ]},
    {"icon": "🥇", "name": "Precious Metals", "assets": [
        ("Gold", "GC=F"),
        ("Silver", "SI=F"),
        ("Platinum", "PL=F"),
        ("Palladium", "PA=F")
    ]},
    {"icon": "🛢️", "name": "Energy Futures", "assets": [
        ("Crude Oil WTI", "CL=F"),
        ("Brent Crude", "BZ=F"),
        ("Natural Gas", "NG=F"),
        ("Heating Oil", "HO=F"),
        ("RBOB Gasoline", "RB=F")
    ]},
    {"icon": "🌾", "name": "Grains & Softs", "assets": [
        ("Corn", "ZC=F"),
        ("Soybeans", "ZS=F"),
        ("Wheat", "ZW=F"),
        ("Coffee", "KC=F"),
        ("Sugar", "SB=F"),
        ("Cotton", "CT=F"),
        ("Cocoa", "CC=F")
    ]},
    {"icon": "🔩", "name": "Industrial Metals", "assets": [
        ("Copper", "HG=F"),
        ("Aluminium", "ALI=F")
    ]},
    {"icon": "📈", "name": "US Stocks", "assets": [
        ("Apple", "AAPL"),
        ("Microsoft", "MSFT"),
        ("Google", "GOOGL"),
        ("Amazon", "AMZN"),
        ("NVIDIA", "NVDA"),
        ("Meta", "META"),
        ("Tesla", "TSLA"),
        ("AMD", "AMD"),
        ("Netflix", "NFLX"),
        ("Oracle", "ORCL"),
        ("JPMorgan", "JPM"),
        ("Goldman Sachs", "GS"),
        ("Johnson & Johnson", "JNJ"),
        ("Pfizer", "PFE"),
        ("Exxon Mobil", "XOM"),
        ("Chevron", "CVX")
    ]},
    {"icon": "🇬🇧", "name": "UK Stocks", "assets": [
        ("Barclays", "BARC.L"),
        ("Lloyds", "LLOY.L"),
        ("HSBC", "HSBA.L"),
        ("GSK", "GSK.L"),
        ("AstraZeneca", "AZN.L")
    ]},
    {"icon": "📊", "name": "Global Indices", "assets": [
        ("S&P 500", "^GSPC"),
        ("Dow Jones", "^DJI"),
        ("Nasdaq", "^IXIC"),
        ("FTSE 100", "^FTSE"),
        ("Nikkei 225", "^N225"),
        ("DAX Germany", "^GDAXI"),
        ("CAC 40 France", "^FCHI")
    ]},
    {"icon": "💱", "name": "Forex Majors", "assets": [
        ("EUR/USD", "EURUSD=X"),
        ("GBP/USD", "GBPUSD=X"),
        ("USD/JPY", "USDJPY=X"),
        ("AUD/USD", "AUDUSD=X"),
        ("USD/CAD", "USDCAD=X"),
        ("EUR/GBP", "EURGBP=X")
    ]},
]

total_assets = sum(len(c["assets"]) for c in CATEGORIES)

# ──────────────────────────────────────────────
# NEON HERO HEADER
# ──────────────────────────────────────────────
st.markdown(f"""
<div class='hero'>
    <div class='hero-icon'>⚡</div>
    <h1 class='hero-title'>QUANTUM PULSE</h1>
    <p class='hero-sub'><span class='dot'></span>MARKET INTELLIGENCE · SIGNAL DETECTION<span class='dot'></span></p>
    <div class='hero-line'></div>
</div>
<div class='stats-bar'>
    <div class='stat-item'><div class='stat-num'>{len(CATEGORIES)}</div><div class='stat-label'>Categories</div></div>
    <div class='stat-item'><div class='stat-num'>{total_assets}</div><div class='stat-label'>Markets Tracked</div></div>
    <div class='stat-item'><div class='stat-num'>3</div><div class='stat-label'>Signal Types</div></div>
    <div class='stat-item'><div class='stat-num'>24/7</div><div class='stat-label'>On Demand</div></div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CARD GRID + CENTERED BUTTONS
# ──────────────────────────────────────────────
st.markdown("<div class='section-title'>Select a Market to Scan</div>", unsafe_allow_html=True)

cols = st.columns(3)
for i, cat in enumerate(CATEGORIES):
    with cols[i % 3]:
        st.markdown(f"""
        <div class='cat-card'>
            <div class='cat-icon'>{cat['icon']}</div>
            <div class='cat-name'>{cat['name']}</div>
            <div class='cat-count'>{len(cat['assets'])} assets</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("SCAN", key=f"btn_{cat['name']}"):
            play_pulse_sound()
            st.session_state[f"scanned_{cat['name']}"] = True

# ──────────────────────────────────────────────
# RESULTS
# ──────────────────────────────────────────────
for cat in CATEGORIES:
    if st.session_state.get(f"scanned_{cat['name']}"):
        st.markdown(f"<div class='section-title'>{cat['icon']} {cat['name']} — Results</div>", unsafe_allow_html=True)
        with st.spinner(f"Scanning {cat['name']}..."):
            sigs = []
            for display_name, ticker in cat["assets"]:
                r = get_signal(display_name, ticker)
                if r: sigs.append(r)
        
        if sigs:
            df = pd.DataFrame(sigs)
            st.markdown(render_table(df), unsafe_allow_html=True)
            
            ldf = df[df["_signal_raw"] == "LONG"]
            sdf = df[df["_signal_raw"] == "SHORT"]
            
            c1, c2 = st.columns(2)
            with c1:
                if len(ldf) > 0:
                    st.markdown(f"<div class='summary-card summary-long'><div class='summary-title' style='color:#34d399;'>▲ {len(ldf)} Long Signals</div>", unsafe_allow_html=True)
                    for _, r in ldf.iterrows():
                        st.markdown(f"<span class='ticker mono'>{r['Asset']}</span> &nbsp; <span class='pos'>+{r['1M %']}% 1M</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("No Long signals")
            with c2:
                if len(sdf) > 0:
                    st.markdown(f"<div class='summary-card summary-short'><div class='summary-title' style='color:#f87171;'>▼ {len(sdf)} Short Signals</div>", unsafe_allow_html=True)
                    for _, r in sdf.iterrows():
                        st.markdown(f"<span class='ticker mono'>{r['Asset']}</span> &nbsp; <span class='neg'>{r['1M %']}% 1M</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("No Short signals")
        else:
            st.info("No signals found right now")
        
        st.session_state[f"scanned_{cat['name']}"] = False
        st.divider()

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    ⚡ QUANTUM PULSE · Market Intelligence Platform<br>
    <span style='font-size:0.7rem;'>For educational purposes only. Not financial advice.</span>
</div>
""", unsafe_allow_html=True)