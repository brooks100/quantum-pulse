from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
import yfinance as yf

# ✅ FREE LOCAL AI — NO KEY NEEDED
local_llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

@tool
def scan_ticker(ticker: str) -> str:
    """Get price, volume and trend for a ticker symbol"""
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="1mo")
        if hist.empty:
            return f"No data found for {ticker}"
        latest = hist.iloc[-1]
        change = ((latest['Close'] - hist.iloc[0]['Close']) / hist.iloc[0]['Close']) * 100
        return f"""
Ticker: {ticker}
Price: ${latest['Close']:.2f}
1-Month Change: {change:.2f}%
Volume: {int(latest['Volume']):,}
"""
    except Exception as e:
        return f"Error fetching {ticker}: {str(e)}"

@tool
def check_risk(confidence: float, position_size_pct: float) -> str:
    """Check if trade is within risk limits — returns APPROVED or REJECTED"""
    if position_size_pct > 0.05:
        return "REJECTED: Position too big (max 5%)"
    if confidence < 0.7:
        return "REJECTED: Confidence too low (min 70%)"
    return "✅ APPROVED"

# --- AGENTS — all use FREE local AI ---
scanner = Agent(
    role="Market Scanner",
    llm=local_llm,
    goal="Scan watchlist and report price, trend and volume",
    backstory="You monitor markets and spot interesting price action.",
    tools=[scan_ticker],
    verbose=True
)

manager = Agent(
    role="Portfolio Manager",
    llm=local_llm,
    goal="Analyze scan results and suggest trades with confidence and position sizes",
    backstory="You balance opportunity against risk.",
    verbose=True
)

risk = Agent(
    role="Risk Manager",
    llm=local_llm,
    goal="Enforce risk rules and approve or reject trades",
    backstory="You protect capital — no exceptions.",
    tools=[check_risk],
    verbose=True
)

# --- TASKS ---
scan_task = Task(
    description="Scan: AAPL, MSFT, BTC-USD, ETH-USD. For each give price, 1-month change, trend direction. List top 2 candidates.",
    expected_output="Summary per ticker + top picks",
    agent=scanner
)

pick_task = Task(
    description="From the scan results: list each candidate — ticker, buy/sell, confidence 0-1, suggested position % of portfolio.",
    expected_output="Trade candidates list",
    agent=manager
)

approve_task = Task(
    description="Review each candidate trade using check_risk. Show final approved trades only.",
    expected_output="Final trade plan",
    agent=risk
)

# --- RUN ---
if __name__ == "__main__":
    print("🚀 Starting your AI Mini Hedge Fund (FREE Local AI)...\n")
    crew = Crew(
        agents=[scanner, manager, risk],
        tasks=[scan_task, pick_task, approve_task],
        verbose=True
    )
    result = crew.kickoff()
    print("\n" + "="*50)
    print("📊 FINAL TRADE PLAN")
    print("="*50)
    print(result)