import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.express as px
import base64
import struct
import math

# ──────────────────────────────────────────────
# FORCE DARK MODE FIRST — nothing can override this
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="QUANTUM PULSE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force dark theme at the very top
st.markdown('<style>:root{color-scheme:dark;}</style>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# THEME — full dark styling
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

* { font-family: 'Space Grotesk', sans-serif; }
code, .mono { font-family: 'JetBrains Mono', monospace; }

.stApp {
    background: 
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,240,255,0.08), transparent),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(168,85,247,0.08), transparent),
        radial-gradient(ellipse 60% 40% at 20% 100%, rgba(255,0,170,0.06), transparent),
        #050510;
    color: #e8e8ff;
}

[data-testid="stSidebar"] {
    background: rgba(10,10,25,0.85);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0,240,255,0.15);
}

.app-title {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 4rem;
    text-align: center;
    letter-spacing: 0.35em;
    line-height: 1;
    margin: 0.5rem 0 0.2rem 0;
    background: linear-gradient(135deg, #00f0ff 0%, #7c3aed 50%, #ff00aa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 30px rgba(0,240,255,0.4));
    animation: titleShimmer 3s ease-in-out infinite;
}

@keyframes titleShimmer {
    0%, 100% { filter: drop-shadow(0 0 20px rgba(0,240,255,0.3)); }
    50% { filter: drop-shadow(0 0 40px rgba(124,58,237,0.5)); }
}

.app-subtitle {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.5em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 2rem;
}

.pulse-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #00f0ff, #7c3aed, #ff00aa, transparent);
    background-size: 200% 100%;
    animation: pulseSlide 3s linear infinite;
    margin: 0 auto 2rem auto;
    width: 60%;
    border-radius: 2px;
}

@keyframes pulseSlide {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

.glass-card {
    background: rgba(20,20,45,0.5);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.glass-card:hover {
    border-color: rgba(0,240,255,0.3);
    transform: translateY(-3px);
    box-shadow: 0 10px 40px rgba(0,240,255,0.1);
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,240,255,0.5), transparent);
}

.card-label {
    color: #6b7280;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.4rem;
}
.card-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #f0f0ff;
    line-height: 1.1;
}

.stButton > button {
    background: linear-gradient(135deg, #00f0ff 0%, #7c3aed 50%, #ff00aa 100%);
    background-size: 200% 200%;
    color: #ffffff;
    border: none;
    border-radius: 14px;
    padding: 1rem 2.5rem;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    box-shadow: 0 0 30px rgba(0,240,255,0.25), 0 0 60px rgba(124,58,237,0.15);
    width: 100%;
    transition: all 0.3s ease;
    animation: btnGradient 4s ease infinite;
}
@keyframes btnGradient {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 0 50px rgba(0,240,255,0.5), 0 0 80px rgba(124,58,237,0.3);
}
.stButton > button:active { transform: scale(0.98); }

.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.4rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #e0e0ff;
    margin: 1.5rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.section-header::before {
    content: '';
    width: 4px;
    height: 24px;
    background: linear-gradient(180deg, #00f0ff, #7c3aed);
    border-radius: 2px;
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    background-color: #101025 !important;
}
[data-testid="stDataFrame"] table { color: #e8e8ff !important; }
[data-testid="stDataFrame"] th { 
    background-color: #1a1a3a !important; 
    color: #00f0ff !important;
}
[data-testid="stDataFrame"] tr:nth-child(even) { background-color: #151530 !important; }
[data-testid="stDataFrame"] tr:nth-child(odd) { background-color: #101025 !important; }

/* Hide top-right menu & footer */
#MainMenu { visibility: hidden; display: none; }
.stDeployButton { display: none !important; }
footer { visibility: hidden; display: none; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(20,20,45,0.6) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e0e0ff !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #00f0ff !important;
    box-shadow: 0 0 15px rgba(0,240,255,0.2) !important;
}

.stSelectbox > div > div > div {
    background: rgba(20,20,45,0.6) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
}

.stMetric { background-color: transparent !important; }
.stMarkdown, .stText { color: #e8e8ff !important; }
div[data-testid="stMarkdownContainer"] { color: #e8e8ff !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────
for key in ['portfolio', 'journal', 'history']:
    if key not in st.session_state:
        st.session_state[key] = {} if key == 'portfolio' else []
if 'starting_balance' not in st.session_state:
    st.session_state.starting_balance = 1000.0

# ──────────────────────────────────────────────
# SCAN FUNCTION
# ──────────────────────────────────────────────
def get_signal(ticker):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="3mo")
        if hist.empty or len(hist) < 5:
            return None
        price = hist.iloc[-1]['Close']
        chg_1w = ((price - hist.iloc[-5]['Close']) / hist.iloc[-5]['Close']) * 100 if len(hist) >= 5 else 0
        chg_1m = ((price - hist.iloc[0]['Close']) / hist.iloc[0]['Close']) * 100
        ma20 = hist['Close'].tail(20).mean()
        above_ma = price > ma20
        recent_high = hist['High'].tail(10).max()
        dd = ((price - recent_high) / recent_high) * 100

        if above_ma and chg_1w > 0 and chg_1m > 0:
            signal = "LONG"
        elif (not above_ma) or (chg_1w < -3) or (dd < -8):
            signal = "SHORT"
        else:
            signal = "HOLD"

        return {
            "Asset": ticker,
            "Price": round(price, 2),
            "1W %": round(chg_1w, 2),
            "1M %": round(chg_1m, 2),
            "Signal": signal
        }
    except:
        return None

# ──────────────────────────────────────────────
# ASSET LIST
# ──────────────────────────────────────────────
STOCKS = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AMD", "NFLX",
    "ORCL", "CRM", "ADBE", "INTC", "IBM", "QCOM", "TXN", "AVGO",
    "JPM", "BAC", "GS", "MS", "C", "WFC", "AXP", "BLK", "SPGI", "CME",
    "JNJ", "PFE", "MRK", "ABBV", "TMO", "UNH", "CVS", "MCK", "AMGN", "GILD",
    "WMT", "COST", "HD", "MCD", "SBUX", "NKE", "DIS", "CMCSA", "V", "MA",
    "PG", "KO", "PEP", "MO", "PM", "CL", "KMB", "KR", "TGT", "LOW",
    "XOM", "CVX", "COP", "EOG", "PXD", "OXY", "SLB", "HAL", "BKR", "VLO",
    "BA", "CAT", "GE", "HON", "UNP", "FDX", "UPS", "DE", "NEE", "DUK",
    "HSBC", "BARC", "LLOY", "RIO", "BHP", "BP", "SHEL", "VOD", "GSK", "AZN"
]
COMMODITIES = ["GC=F", "SI=F", "PL=F", "PA=F", "CL=F", "BZ=F", "NG=F", "HG=F", "ZC=F", "ZS=F", "ZW=F", "KC=F", "SB=F"]
CRYPTO = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", "DOT-USD", "MATIC-USD", "LINK-USD", "UNI-USD", "ATOM-USD", "NEAR-USD", "OP-USD", "ARB-USD", "FIL-USD", "ICP-USD", "VET-USD", "AAVE-USD", "GRT-USD", "SHIB-USD", "PEPE-USD", "BONK-USD", "FLOKI-USD"]
INDICES = ["^GSPC", "^DJI", "^IXIC", "^RUT", "^FTSE", "^N225", "^HSI", "^SSEC", "^KS11", "^AXJO", "^BVSP", "^MXX", "^VIX"]
FOREX = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "EURGBP=X", "EURJPY=X", "GBPJPY=X", "USDCHF=X", "NZDUSD=X"]

tickers_list = list(set(STOCKS + COMMODITIES + CRYPTO + INDICES + FOREX))
tickers_list = [t for t in tickers_list if t]

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:Rajdhani; font-size:1.3rem; font-weight:700; text-align:center; letter-spacing:0.2em; color:#00f0ff;">⚡ CONTROL PANEL</p>', unsafe_allow_html=True)
    st.markdown('<div class="pulse-line" style="width:100%; margin:0.5rem 0;"></div>', unsafe_allow_html=True)
    
    st.markdown(f"**📊 TOTAL ASSETS:** `{len(tickers_list)}`")
    st.caption(f"Stocks {len(set(STOCKS))} · Commodities {len(set(COMMODITIES))} · Crypto {len(CRYPTO)} · Indices {len(INDICES)} · Forex {len(FOREX)}")
    
    st.markdown('<div class="pulse-line" style="width:100%; margin:1rem 0;"></div>', unsafe_allow_html=True)
    st.markdown("**⚙️ RISK SETTINGS**")
    max_risk_pct = st.slider("Max Single Trade Risk %", 1, 5, 2)
    st.info("💡 Start at £0.50–£1.00 per point. Always set Stop Loss.")

# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
st.markdown("""
<h1 class="app-title">QUANTUM PULSE</h1>
<div class="pulse-line"></div>
<p class="app-subtitle">AI Market Scanner · Signal Detection · Spread Betting Terminal</p>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# PERFORMANCE CARDS
# ──────────────────────────────────────────────
closed = [j for j in st.session_state.journal if j.get('status') == 'CLOSED']
total_pnl = sum(t.get('pnl', 0) for t in closed)
wins = sum(1 for t in closed if t.get('pnl', 0) > 0)
win_rate = (wins / len(closed) * 100) if closed else 0
balance = st.session_state.starting_balance + total_pnl

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="glass-card"><div class="card-label">Virtual Balance</div><div class="card-value">£{balance:,.2f}</div></div>', unsafe_allow_html=True)
with c2:
    pnl_col = "#00ff88" if total_pnl >= 0 else "#ff4466"
    st.markdown(f'<div class="glass-card"><div class="card-label">Total P&L</div><div class="card-value" style="color:{pnl_col}">£{total_pnl:+,.2f}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="glass-card"><div class="card-label">Win Rate</div><div class="card-value">{win_rate:.0f}%</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="glass-card"><div class="card-label">Open Bets</div><div class="card-value">{len(st.session_state.portfolio)}</div></div>', unsafe_allow_html=True)

st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SCAN BUTTON
# ──────────────────────────────────────────────
scan_now = st.button("⚡ INITIATE QUANTUM SCAN — ALL MARKETS")
signals = []

if scan_now:
    scan_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f'<p style="color:#00f0ff; font-family:JetBrains Mono; font-size:0.85rem;">▸ SCAN INITIATED · {scan_time} · {len(tickers_list)} ASSETS</p>', unsafe_allow_html=True)
    
    progress = st.progress(0)
    status_text = st.empty()
    for idx, t in enumerate(tickers_list):
        result = get_signal(t)
        if result:
            signals.append(result)
        progress.progress((idx + 1) / len(tickers_list))
        status_text.markdown(f"<p style='color:#666; font-size:0.75rem; font-family:JetBrains Mono;'>Scanning: {t} ({idx+1}/{len(tickers_list)})</p>", unsafe_allow_html=True)
    
    status_text.empty()
    st.session_state.history.append({"time": scan_time, "count": len(signals)})
    st.success(f"✅ SCAN COMPLETE — {len(signals)} of {len(tickers_list)} assets found")
else:
    st.info("👆 Click the scan button — all markets will be analyzed")

# ──────────────────────────────────────────────
# SIGNAL MATRIX
# ──────────────────────────────────────────────
if signals:
    st.markdown('<div class="section-header">Live Signal Matrix</div>', unsafe_allow_html=True)
    st.caption("🟢 LONG = Buy/Up | 🟡 HOLD = Keep | 🔴 SHORT = Sell/Down")

    df = pd.DataFrame(signals)
    
    def color_sig(val):
        if val == "LONG": return 'color: #00ff88; font-weight: bold'
        elif val == "SHORT": return 'color: #ff4466; font-weight: bold'
        return 'color: #ffc107; font-weight: bold'
    
    st.dataframe(
        df.style.map(color_sig, subset=["Signal"]),
        width='stretch',
        hide_index=True
    )

    st.markdown('<div class="section-header">Top Opportunities</div>', unsafe_allow_html=True)
    long_df = df[df["Signal"] == "LONG"].sort_values("1M %", ascending=False).head(10)
    short_df = df[df["Signal"] == "SHORT"].sort_values("1M %", ascending=True).head(10)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🟢 Top LONG (Buy)**")
        if len(long_df):
            st.dataframe(long_df[["Asset","Price","1W %","1M %"]], width='stretch', hide_index=True)
        else:
            st.info("No LONG signals yet")
    with col2:
        st.markdown("**🔴 Top SHORT (Sell)**")
        if len(short_df):
            st.dataframe(short_df[["Asset","Price","1W %","1M %"]], width='stretch', hide_index=True)
        else:
            st.info("No SHORT signals yet")

    st.markdown('<div class="section-header">30-Day Momentum</div>', unsafe_allow_html=True)
    chart_df = df.sort_values("1M %", ascending=False)
    fig = px.bar(
        chart_df, x="Asset", y="1M %", color="1M %",
        color_continuous_scale=["#ff4466", "#334155", "#00ff88"],
        template="plotly_dark",
        height=550
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        xaxis_tickangle=-45,
        font=dict(family="Space Grotesk", size=11)
    )
    st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# BET JOURNAL
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">Spread Bet Journal</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([1, 2])
with col_a:
    with st.form("open_bet"):
        st.markdown("**Log New Bet**")
        tkr = st.text_input("Market / Ticker", placeholder="e.g. GC=F, EURUSD=X, AAPL")
        direction = st.selectbox("Direction", ["LONG (Buy/Up)", "SHORT (Sell/Down)"])
        entry_price = st.number_input("Entry Price", 0.0, step=0.01)
        stake_per_point = st.number_input("Stake £ per Point", 0.01, step=0.01, value=0.50)
        reason = st.text_input("Signal / Reason", placeholder="e.g. LONG — strong momentum")
        
        if st.form_submit_button("✅ LOG BET") and tkr:
            dir_short = "LONG" if "LONG" in direction else "SHORT"
            st.session_state.portfolio[tkr.upper()] = {
                "direction": dir_short, "entry": entry_price, "stake": stake_per_point,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state.journal.append({
                "ticker": tkr.upper(), "direction": dir_short, "entry": entry_price,
                "stake": stake_per_point, "entry_date": datetime.now().strftime("%Y-%m-%d"),
                "reason": reason, "status": "OPEN"
            })
            st.success(f"Logged {dir_short} bet on {tkr.upper()}")
            st.rerun()

with col_b:
    if st.session_state.portfolio:
        st.markdown("**Open Positions**")
        port_rows = []
        for t, info in st.session_state.portfolio.items():
            try:
                data = yf.Ticker(t)
                hist = data.history(period="3mo")
                cur = hist.iloc[-1]['Close'] if not hist.empty else info['entry']
                pnl = (cur - info['entry']) * info['stake'] if info['direction'] == "LONG" else (info['entry'] - cur) * info['stake']
                chg_1w = ((cur - hist.iloc[-5]['Close']) / hist.iloc[-5]['Close']) * 100 if len(hist)>=5 else 0
                ma20 = hist['Close'].tail(20).mean() if len(hist)>=20 else cur
                dd = ((cur - hist['High'].tail(10).max()) / hist['High'].tail(10).max()) * 100 if len(hist)>=10 else 0
                exit_sig = "CLOSE" if (
                    (info['direction'] == "LONG" and (cur < ma20 or chg_1w < -3 or dd < -8)) or
                    (info['direction'] == "SHORT" and (cur > ma20 or chg_1w > 3))
                ) else "HOLD"
                port_rows.append({
                    "Market": t, "Dir": info['direction'], "£/pt": f"£{info['stake']}",
                    "Entry": f"{info['entry']:.2f}", "Now": f"{cur:.2f}",
                    "P&L": f"£{pnl:+,.2f}", "Action": exit_sig
                })
            except: pass
        
        if port_rows:
            st.dataframe(pd.DataFrame(port_rows), width='stretch', hide_index=True)
            close_t = st.selectbox("Close bet:", [""] + list(st.session_state.portfolio.keys()))
            exit_price = st.number_input("Exit Price", 0.0, step=0.01)
            if close_t and st.button("🔒 SETTLE BET"):
                info = st.session_state.portfolio[close_t]
                pnl = (exit_price - info['entry']) * info['stake'] if info['direction'] == "LONG" else (info['entry'] - exit_price) * info['stake']
                for j in st.session_state.journal:
                    if j.get('ticker') == close_t and j.get('status') == 'OPEN':
                        j['exit'] = exit_price; j['pnl'] = pnl; j['status'] = 'CLOSED'; break
                del st.session_state.portfolio[close_t]
                st.rerun()
    else:
        st.info("No open bets yet. Run scan → get signal → place in IG/Spreadex → log here.")

if closed:
    st.markdown('<div class="section-header">Settled Bets</div>', unsafe_allow_html=True)
    jdf = pd.DataFrame(closed)
    keep_cols = [c for c in ["ticker","direction","entry_date","stake","entry","exit","pnl"] if c in jdf.columns]
    st.dataframe(jdf[keep_cols], width='stretch', hide_index=True)

st.markdown('<div style="height:2rem;"></div>', unsafe_allow_html=True)
st.caption("⚡ QUANTUM PULSE · 100+ Assets · Not financial advice · Check IG/Spreadex symbol names may differ")
