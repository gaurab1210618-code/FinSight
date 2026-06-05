# ============================================================
#  FinSight AI Dashboard  -  app.py (Free Presentation Version)
#  Production-ready Streamlit financial intelligence platform
# ============================================================

import io
import json
import math
import time
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from fpdf import FPDF

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FinSight AI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  - dark dashboard aesthetic
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #58a6ff;
}

/* ── Metric Cards ── */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(88,166,255,0.12);
    border-color: #58a6ff;
}
div[data-testid="metric-container"] label {
    color: #8b949e !important;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e6edf3 !important;
    font-size: 1.6rem;
    font-weight: 700;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.82rem;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.15rem;
    font-weight: 700;
    color: #58a6ff;
    letter-spacing: 0.03em;
    padding: 6px 0 10px 0;
    border-bottom: 2px solid #21262d;
    margin-bottom: 16px;
}

/* ── Card containers ── */
.card {
    background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 22px 26px;
    margin: 10px 0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35);
}

/* ── AI Recommendation Card ── */
.ai-card {
    background: linear-gradient(135deg, #0d2137 0%, #0a1628 100%);
    border: 1px solid #1f6feb;
    border-radius: 14px;
    padding: 24px 28px;
    margin: 12px 0;
    box-shadow: 0 0 32px rgba(31,111,235,0.15);
}
.rec-badge-buy {
    background: linear-gradient(135deg, #238636, #2ea043);
    color: white;
    padding: 8px 24px;
    border-radius: 20px;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    display: inline-block;
    box-shadow: 0 4px 16px rgba(46,160,67,0.35);
}
.rec-badge-hold {
    background: linear-gradient(135deg, #9e6a03, #d29922);
    color: white;
    padding: 8px 24px;
    border-radius: 20px;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    display: inline-block;
    box-shadow: 0 4px 16px rgba(210,153,34,0.35);
}
.rec-badge-sell {
    background: linear-gradient(135deg, #b91c1c, #da3633);
    color: white;
    padding: 8px 24px;
    border-radius: 20px;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    display: inline-block;
    box-shadow: 0 4px 16px rgba(218,54,51,0.35);
}

/* ── Chat Bubbles ── */
.chat-user {
    background: linear-gradient(135deg, #1f3a5f, #1a3354);
    border: 1px solid #1f6feb;
    border-radius: 12px 12px 2px 12px;
    padding: 12px 18px;
    margin: 8px 0;
    color: #cdd9e5;
}
.chat-ai {
    background: linear-gradient(135deg, #161b22, #1c2128);
    border: 1px solid #30363d;
    border-radius: 12px 12px 12px 2px;
    padding: 12px 18px;
    margin: 8px 0;
    color: #e6edf3;
}

/* ── Plotly chart backgrounds ── */
.js-plotly-plot .plotly .main-svg {
    background: transparent !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-radius: 10px;
    gap: 4px;
    padding: 4px;
    border: 1px solid #21262d;
}
.stTabs [data-baseweb="tab"] {
    color: #8b949e;
    border-radius: 8px;
    font-weight: 500;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1f6feb, #388bfd) !important;
    color: white !important;
    font-weight: 600;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1f6feb, #388bfd);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 24px;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(31,111,235,0.25);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(31,111,235,0.4);
    background: linear-gradient(135deg, #388bfd, #58a6ff);
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #161b22;
    border: 2px dashed #30363d;
    border-radius: 12px;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #58a6ff;
}

/* ── Divider ── */
hr {
    border-color: #21262d !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #161b22 !important;
    border-radius: 8px !important;
    color: #8b949e !important;
}

/* ── Warning / Info / Success ── */
.stAlert {
    border-radius: 10px !important;
}

/* ── Status indicator dot ── */
.status-dot-green {
    display: inline-block;
    width: 8px; height: 8px;
    background: #3fb950;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
.status-dot-yellow {
    display: inline-block;
    width: 8px; height: 8px;
    background: #d29922;
    border-radius: 50%;
    margin-right: 6px;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Logo text ── */
.logo-text {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #58a6ff, #79c0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.02em;
}
.logo-sub {
    font-size: 0.72rem;
    color: #8b949e;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ── Scenario cards ── */
.scenario-bull {
    background: linear-gradient(135deg, #0d2b0d, #0f3d0f);
    border-left: 4px solid #3fb950;
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
    margin: 8px 0;
}
.scenario-base {
    background: linear-gradient(135deg, #0d1a2d, #0a1628);
    border-left: 4px solid #58a6ff;
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
    margin: 8px 0;
}
.scenario-bear {
    background: linear-gradient(135deg, #2d0d0d, #3d0f0f);
    border-left: 4px solid #f85149;
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
    margin: 8px 0;
}
</style>
""",
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════
#  HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#8b949e", family="Inter"),
    margin=dict(l=16, r=16, t=40, b=16),
    legend=dict(
        bgcolor="rgba(22,27,34,0.8)",
        bordercolor="#30363d",
        borderwidth=1,
    ),
)

BLUE_PALETTE = ["#58a6ff", "#388bfd", "#1f6feb", "#79c0ff", "#a5d6ff"]
GREEN_PALETTE = ["#3fb950", "#2ea043", "#238636"]
RED_PALETTE = ["#f85149", "#da3633", "#b91c1c"]


def fmt_large(val):
    """Format large numbers with B/M/K suffix."""
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return "N/A"
    val = float(val)
    if abs(val) >= 1e9:
        return f"{val/1e9:.2f}B"
    if abs(val) >= 1e6:
        return f"{val/1e6:.2f}M"
    if abs(val) >= 1e3:
        return f"{val/1e3:.1f}K"
    return f"{val:.2f}"


def safe_div(a, b, default=None):
    try:
        if b == 0 or b is None or (isinstance(b, float) and math.isnan(b)):
            return default
        return a / b
    except Exception:
        return default


def col_search(df, *candidates):
    """Return the first column in df that matches any candidate (case-insensitive)."""
    lower_cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lower_cols:
            return lower_cols[cand.lower()]
    return None


def load_file(uploaded_file):
    """Load CSV or Excel file into a DataFrame."""
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        df.columns = [str(c).strip() for c in df.columns]
        # Try to parse numeric columns
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="ignore")
            except Exception:
                pass
        return df
    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
#  RATIO ENGINE  (pure Python / pandas - no external API)
# ═══════════════════════════════════════════════════════════════

def compute_ratios(df: pd.DataFrame) -> dict:
    """
    Dynamically detect financial columns and compute standard ratios.
    Returns a dict with ratio groups and individual values.
    """
    c = {}  # shorthand column lookup

    # ── Revenue / Income ──
    c["revenue"]       = col_search(df, "revenue", "total revenue", "net revenue", "sales", "net sales", "turnover")
    c["net_income"]    = col_search(df, "net income", "net profit", "profit after tax", "pat", "earnings", "net earnings")
    c["gross_profit"]  = col_search(df, "gross profit", "gross income")
    c["ebit"]          = col_search(df, "ebit", "operating income", "operating profit")
    c["ebitda"]        = col_search(df, "ebitda")

    # ── Balance Sheet ──
    c["total_assets"]  = col_search(df, "total assets", "assets")
    c["total_equity"]  = col_search(df, "total equity", "shareholders equity", "stockholders equity", "equity")
    c["total_debt"]    = col_search(df, "total debt", "long term debt", "debt", "borrowings")
    c["curr_assets"]   = col_search(df, "current assets", "total current assets")
    c["curr_liab"]     = col_search(df, "current liabilities", "total current liabilities")
    c["inventory"]     = col_search(df, "inventory", "inventories")
    c["cash"]          = col_search(df, "cash", "cash and cash equivalents", "cash equivalents")

    # ── Market / Per Share ──
    c["eps"]           = col_search(df, "eps", "earnings per share", "diluted eps")
    c["market_cap"]    = col_search(df, "market cap", "market capitalization")
    c["price"]         = col_search(df, "price", "stock price", "share price", "closing price")
    c["shares"]        = col_search(df, "shares", "shares outstanding", "diluted shares")

    # ── Year column ──
    c["year"]          = col_search(df, "year", "fiscal year", "fy", "period", "date")

    def latest(col_name):
        if col_name and col_name in df.columns:
            series = pd.to_numeric(df[col_name], errors="coerce").dropna()
            return series.iloc[-1] if len(series) > 0 else None
        return None

    rev    = latest(c["revenue"])
    ni     = latest(c["net_income"])
    gp     = latest(c["gross_profit"])
    ebit   = latest(c["ebit"])
    ta     = latest(c["total_assets"])
    eq     = latest(c["total_equity"])
    debt   = latest(c["total_debt"])
    ca     = latest(c["curr_assets"])
    cl     = latest(c["curr_liab"])
    inv    = latest(c["inventory"])
    eps    = latest(c["eps"])
    price  = latest(c["price"])
    mc     = latest(c["market_cap"])

    ratios = {}

    # ── Liquidity ──
    ratios["current_ratio"]  = safe_div(ca, cl)
    ratios["quick_ratio"]    = safe_div((ca - inv) if (ca and inv) else ca, cl)
    ratios["cash_ratio"]     = safe_div(latest(c["cash"]), cl)

    # ── Profitability ──
    ratios["gross_margin"]   = safe_div(gp, rev)
    ratios["net_margin"]     = safe_div(ni, rev)
    ratios["ebit_margin"]    = safe_div(ebit, rev)
    ratios["roe"]            = safe_div(ni, eq)
    ratios["roa"]            = safe_div(ni, ta)

    # ── Leverage ──
    ratios["de_ratio"]       = safe_div(debt, eq)
    ratios["debt_to_assets"] = safe_div(debt, ta)
    interest = col_search(df, "interest expense", "finance costs", "interest")
    ratios["interest_coverage"] = safe_div(ebit, latest(interest))

    # ── Valuation ──
    ratios["pe_ratio"]       = safe_div(price, eps) if (price and eps) else safe_div(mc, ni)
    ratios["pb_ratio"]       = safe_div(mc, eq) if (mc and eq) else None
    ratios["ps_ratio"]       = safe_div(mc, rev) if (mc and rev) else None
    ratios["ev_ebitda"]      = None  # Would need EV; skip if not available

    # ── YoY Growth (last two periods) ──
    def yoy(col_name):
        if col_name and col_name in df.columns:
            s = pd.to_numeric(df[col_name], errors="coerce").dropna()
            if len(s) >= 2:
                return safe_div(s.iloc[-1] - s.iloc[-2], abs(s.iloc[-2]))
        return None

    ratios["revenue_growth"]    = yoy(c["revenue"])
    ratios["ni_growth"]         = yoy(c["net_income"])
    ratios["asset_growth"]      = yoy(c["total_assets"])

    # ── Risk Score (0-100, higher = riskier) ──
    risk = 50.0  # baseline
    if ratios["current_ratio"] is not None:
        risk -= min(10, (ratios["current_ratio"] - 1) * 5)
    if ratios["de_ratio"] is not None:
        risk += min(15, ratios["de_ratio"] * 5)
    if ratios["net_margin"] is not None:
        risk -= min(10, ratios["net_margin"] * 100)
    if ratios["roe"] is not None:
        risk -= min(10, ratios["roe"] * 50)
    if ratios["revenue_growth"] is not None:
        risk -= min(10, ratios["revenue_growth"] * 30)
    ratios["risk_score"] = max(0, min(100, risk))

    return ratios, c


# ═══════════════════════════════════════════════════════════════
#  PLOTLY CHART BUILDERS
# ═══════════════════════════════════════════════════════════════

def chart_revenue_trend(df, year_col, rev_col):
    years = df[year_col].astype(str)
    rev   = pd.to_numeric(df[rev_col], errors="coerce")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=rev,
        mode="lines+markers",
        name="Revenue",
        line=dict(color="#58a6ff", width=3),
        marker=dict(size=8, color="#58a6ff", line=dict(color="#0d1117", width=2)),
        fill="tozeroy",
        fillcolor="rgba(88,166,255,0.08)",
    ))
    fig.update_layout(
        title=dict(text="📈 Revenue Trend", font=dict(size=15, color="#e6edf3")),
        xaxis=dict(title="Year", gridcolor="#21262d", linecolor="#30363d"),
        yaxis=dict(title="Revenue", gridcolor="#21262d", linecolor="#30363d", tickformat=".3s"),
        **PLOTLY_LAYOUT,
    )
    return fig


def chart_yoy_growth(df, year_col, cols):
    valid_cols = [(label, c) for label, c in cols if c and c in df.columns]
    if not valid_cols:
        return None

    years = df[year_col].astype(str).tolist()
    fig = go.Figure()
    palette = BLUE_PALETTE + GREEN_PALETTE
    for i, (label, col) in enumerate(valid_cols):
        vals = pd.to_numeric(df[col], errors="coerce")
        growth = vals.pct_change() * 100
        fig.add_trace(go.Bar(
            x=years, y=growth,
            name=label,
            marker_color=palette[i % len(palette)],
            opacity=0.85,
        ))
    fig.update_layout(
        title=dict(text="📊 YoY Growth (%)", font=dict(size=15, color="#e6edf3")),
        xaxis=dict(title="Year", gridcolor="#21262d", linecolor="#30363d"),
        yaxis=dict(title="Growth %", gridcolor="#21262d", linecolor="#30363d"),
        barmode="group",
        **PLOTLY_LAYOUT,
    )
    return fig


def chart_risk_gauge(risk_score: float):
    if risk_score <= 33:
        gauge_color = "#3fb950"
        label = "LOW RISK"
    elif risk_score <= 66:
        gauge_color = "#d29922"
        label = "MEDIUM RISK"
    else:
        gauge_color = "#f85149"
        label = "HIGH RISK"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        title=dict(text=f"Risk Score  ·  <b>{label}</b>", font=dict(size=14, color="#e6edf3")),
        number=dict(font=dict(size=40, color=gauge_color), suffix="/100"),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#30363d", tickfont=dict(color="#8b949e")),
            bar=dict(color=gauge_color, thickness=0.25),
            bgcolor="rgba(22,27,34,0.8)",
            borderwidth=1,
            bordercolor="#30363d",
            steps=[
                dict(range=[0, 33],  color="rgba(63,185,80,0.15)"),
                dict(range=[33, 66], color="rgba(210,153,34,0.15)"),
                dict(range=[66, 100],color="rgba(248,81,73,0.15)"),
            ],
            threshold=dict(
                line=dict(color=gauge_color, width=3),
                thickness=0.75,
                value=risk_score,
            ),
        ),
    ))
    gauge_layout = {k: v for k, v in PLOTLY_LAYOUT.items() if k != "margin"}
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=40, b=10),
        **gauge_layout,
    )
    return fig


def chart_ratio_radar(ratios: dict):
    cats = []
    vals = []

    mapping = {
        "Current Ratio": ("current_ratio", 3),
        "ROE (x10)":     ("roe", 10),
        "ROA (x10)":     ("roa", 10),
        "Net Margin":    ("net_margin", 100),
        "Gross Margin":  ("gross_margin", 100),
    }

    for label, (key, mult) in mapping.items():
        v = ratios.get(key)
        if v is not None:
            cats.append(label)
            vals.append(min(10, max(0, v * mult)))

    if len(cats) < 3:
        return None

    cats_closed = cats + [cats[0]]
    vals_closed  = vals + [vals[0]]

    fig = go.Figure(go.Scatterpolar(
        r=vals_closed,
        theta=cats_closed,
        fill="toself",
        fillcolor="rgba(88,166,255,0.15)",
        line=dict(color="#58a6ff", width=2),
        marker=dict(size=6, color="#58a6ff"),
    ))
    fig.update_layout(
        title=dict(text="🕸️ Financial Health Radar", font=dict(size=15, color="#e6edf3")),
        polar=dict(
            bgcolor="rgba(22,27,34,0.5)",
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="#21262d", tickcolor="#8b949e"),
            angularaxis=dict(gridcolor="#21262d", tickcolor="#8b949e", tickfont=dict(color="#8b949e")),
        ),
        height=320,
        **PLOTLY_LAYOUT,
    )
    return fig


def chart_competitor_grouped(df1, df2, year_col1, year_col2, rev_col1, rev_col2,
                              name1="Company A", name2="Company B"):
    years1 = df1[year_col1].astype(str) if year_col1 else pd.Series(dtype=str)
    years2 = df2[year_col2].astype(str) if year_col2 else pd.Series(dtype=str)
    rev1   = pd.to_numeric(df1[rev_col1], errors="coerce") if rev_col1 else pd.Series(dtype=float)
    rev2   = pd.to_numeric(df2[rev_col2], errors="coerce") if rev_col2 else pd.Series(dtype=float)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=years1, y=rev1, name=name1, marker_color="#58a6ff", opacity=0.85))
    fig.add_trace(go.Bar(x=years2, y=rev2, name=name2, marker_color="#3fb950", opacity=0.85))

    fig.update_layout(
        title=dict(text="⚔️ Revenue Comparison", font=dict(size=15, color="#e6edf3")),
        xaxis=dict(title="Year", gridcolor="#21262d", linecolor="#30363d"),
        yaxis=dict(title="Revenue", gridcolor="#21262d", linecolor="#30363d", tickformat=".3s"),
        barmode="group",
        **PLOTLY_LAYOUT,
    )
    return fig


def chart_net_income_trend(df, year_col, ni_col):
    years = df[year_col].astype(str)
    ni    = pd.to_numeric(df[ni_col], errors="coerce")
    colors = ["#3fb950" if v >= 0 else "#f85149" for v in ni]

    fig = go.Figure(go.Bar(
        x=years, y=ni,
        marker_color=colors,
        opacity=0.85,
        name="Net Income",
    ))
    fig.update_layout(
        title=dict(text="💰 Net Income Trend", font=dict(size=15, color="#e6edf3")),
        xaxis=dict(title="Year", gridcolor="#21262d", linecolor="#30363d"),
        yaxis=dict(title="Net Income", gridcolor="#21262d", linecolor="#30363d", tickformat=".3s"),
        **PLOTLY_LAYOUT,
    )
    return fig


# ═══════════════════════════════════════════════════════════════
#  AI MOCKUP ENGINE (FREE FOREVER)
# ═══════════════════════════════════════════════════════════════

def get_ai_recommendation(ratios: dict, company_name: str, cache_key: str) -> str:
    """Get BUY/HOLD/SELL mock recommendation."""
    if cache_key in st.session_state.get("ai_cache", {}):
        return st.session_state["ai_cache"][cache_key]
    
    score = ratios.get("risk_score", 50)
    if score <= 40:
        rec, thesis = "BUY", "The company exhibits exceptional profitability metrics and a fortified balance sheet, making it a compelling long-term hold."
    elif score >= 70:
        rec, thesis = "SELL", "Deteriorating leverage ratios and compressed margins present significant downside risk in the near term."
    else:
        rec, thesis = "HOLD", "Fundamentals remain stable, but current valuation suggests limited immediate upside. Monitor upcoming margin performance."

    result = f"""**RECOMMENDATION: {rec}**

**Risk Rating:** {"LOW" if score<=40 else "HIGH" if score>=70 else "MEDIUM"} - Based on multi-factor ratio analysis.
**Target Price Range:** +12% to +18% upside projected.

**Key Strengths:**
• Consistent year-over-year revenue generation.
• Sustainable liquidity buffers protecting against macro shocks.
• Favorable operational margins relative to sector averages.

**Key Risks:**
• Fluctuations in total liabilities require monitoring.
• Sensitivity to interest rate shifts affecting debt overhead.

**Investment Thesis:**
{thesis}"""

    st.session_state["ai_cache"][cache_key] = result
    return result


def get_ai_forecast(df: pd.DataFrame, ratios: dict, company_name: str, cache_key: str) -> str:
    """Get Base/Bull/Bear forecast mock."""
    ck = cache_key + "_forecast"
    if ck in st.session_state.get("ai_cache", {}):
        return st.session_state["ai_cache"][ck]

    result = f"""🐂 **BULL CASE (25% Confidence)**
- Accelerated market capture leading to >15% annualized revenue bumps.
- Margin expansion driven by decreasing cost of goods sold.
- Rapid debt paydown improves leverage flexibility.

📊 **BASE CASE (60% Confidence)**
- Steady top-line growth aligned with historical sector averages.
- Net margins stabilize at current operational levels.
- Balanced capital allocation between reinvestment and equity support.

🐻 **BEAR CASE (15% Confidence)**
- Revenue stagnation due to increased market competition.
- Supply chain pressures force margin compression by 200-300bps.
- Leverage constraints limit future operational pivots.

**Summary:** The base trajectory indicates sustainable, compound growth with manageable structural risks."""
    
    st.session_state["ai_cache"][ck] = result
    return result


def get_ai_competitor_verdict(name1, ratios1, name2, ratios2, cache_key: str) -> str:
    """Get competitor comparison mock verdict."""
    ck = cache_key + "_comp"
    if ck in st.session_state.get("ai_cache", {}):
        return st.session_state["ai_cache"][ck]

    score1 = ratios1.get("risk_score", 50)
    score2 = ratios2.get("risk_score", 50)
    winner = name1 if score1 <= score2 else name2
    loser = name2 if score1 <= score2 else name1

    result = f"""**🏆 WINNER: {winner}**

{winner} demonstrates superior structural efficiency and a more sustainable risk profile compared to {loser}.

**Head-to-Head Highlights:**
- **Profitability:** {winner} shows better core margin protection against operational costs.
- **Liquidity:** Both companies are solvent, but {winner} has a safer capital buffer.
- **Leverage:** {loser} carries a slightly higher systemic debt risk profile.

**Recommendation:** BUY {winner}, WATCH {loser}.

**Thesis:** {winner} represents a robust growth engine with downside protection, whereas {loser} requires tighter operational execution to match intrinsic value."""
    
    st.session_state["ai_cache"][ck] = result
    return result


def get_ai_chat_response(question: str, context: str) -> str:
    """Mock CFO Chatbot."""
    time.sleep(1) # Simulate AI thinking time
    return "Based on the latest financial ratios uploaded to our dashboard, our structural metrics look fundamentally stable. However, keeping an eye on operational efficiency and maintaining our liquidity buffers will be crucial for the next fiscal period. Is there a specific line item from the Income Statement or Balance Sheet you'd like me to break down?"


# ═══════════════════════════════════════════════════════════════
#  PDF EXPORT
# ═══════════════════════════════════════════════════════════════

class FinSightPDF(FPDF):
    def header(self):
        self.set_fill_color(13, 17, 23)
        self.rect(0, 0, 210, 20, "F")
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(88, 166, 255)
        self.set_xy(10, 5)
        self.cell(0, 10, "FinSight AI Dashboard - Financial Report", ln=True)
        self.set_text_color(139, 148, 158)
        self.set_font("Helvetica", "", 8)
        self.set_xy(10, 14)
        self.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(139, 148, 158)
        self.cell(0, 10, f"Page {self.page_no()} | FinSight AI - For informational purposes only", align="C")

    def section_title(self, title):
        self.set_fill_color(22, 27, 34)
        self.set_text_color(88, 166, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 9, title, ln=True, fill=True)
        self.ln(2)

    def body_text(self, text):
        if not text:
            return
        
        # ─── THE INVINCIBLE SANITIZATION SHIELD ───
        safe_text = str(text)
        
        # 1. Keep our professional bullets and clean up markdown
        safe_text = safe_text.replace("•", "- ").replace("▪", "- ").replace("◦", "- ")
        safe_text = safe_text.replace("**", "") 
        safe_text = safe_text.replace("“", '"').replace("”", '"')
        safe_text = safe_text.replace("‘", "'").replace("’", "'")
        safe_text = safe_text.replace("—", "-").replace("–", "-")
        
        # 2. Map known financial emojis to professional text (Optional but looks great)
        safe_text = safe_text.replace("🐂", "[BULLISH] ").replace("🐻", "[BEARISH] ")
        safe_text = safe_text.replace("📈", "[UPWARD] ").replace("📉", "[DOWNWARD] ")
        
        # 3. THE GOD-MODE ENCODING FILTER (Vaporizes ALL remaining unsupported emojis)
        # This translates the text to Latin-1 (which FPDF uses). Any emoji it doesn't 
        # recognize is simply ignored and erased, guaranteeing zero crashes.
        safe_text = safe_text.encode('latin-1', 'ignore').decode('latin-1')
        # ──────────────────────────────────────────

        self.set_text_color(230, 237, 243)
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 5, safe_text)
        self.ln(2)

    def ratio_row(self, label, value, good=None):
        self.set_font("Helvetica", "", 9)
        if good is True:
            self.set_text_color(63, 185, 80)
        elif good is False:
            self.set_text_color(248, 81, 73)
        else:
            self.set_text_color(230, 237, 243)
        self.cell(80, 6, f"  {label}", border=0)
        self.cell(50, 6, str(value), border=0, ln=True)
        self.set_text_color(48, 54, 61)
        self.cell(190, 0.3, "", border=0, ln=True, fill=True)
        self.set_fill_color(48, 54, 61)


def generate_pdf(company_name, ratios, ai_recommendation, ai_forecast, summary_df=None) -> bytes:
    pdf = FinSightPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_fill_color(13, 17, 23)

    pdf.add_page()
    pdf.set_fill_color(13, 17, 23)
    pdf.rect(0, 0, 210, 297, "F")

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(88, 166, 255)
    pdf.ln(4)
    pdf.cell(0, 12, company_name, ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(139, 148, 158)
    pdf.cell(0, 6, "Investment Analysis Report  ·  Powered by FinSight AI", ln=True, align="C")
    pdf.ln(8)

    # Risk Score highlight
    rs = ratios.get("risk_score", 50)
    risk_label = "LOW RISK" if rs <= 33 else ("MEDIUM RISK" if rs <= 66 else "HIGH RISK")
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(230, 237, 243)
    pdf.cell(0, 8, f"Overall Risk Score: {rs:.1f}/100  ({risk_label})", ln=True, align="C")
    pdf.ln(6)

    # ── Key Ratios ──
    pdf.section_title("  KEY FINANCIAL RATIOS")

    groups = {
        "Liquidity": [
            ("Current Ratio",       ratios.get("current_ratio"),     lambda v: v >= 1.5),
            ("Quick Ratio",         ratios.get("quick_ratio"),       lambda v: v >= 1.0),
            ("Cash Ratio",          ratios.get("cash_ratio"),        lambda v: v >= 0.5),
        ],
        "Profitability": [
            ("Gross Margin",        ratios.get("gross_margin"),      lambda v: v >= 0.3),
            ("Net Margin",          ratios.get("net_margin"),        lambda v: v >= 0.1),
            ("ROE",                 ratios.get("roe"),               lambda v: v >= 0.1),
            ("ROA",                 ratios.get("roa"),               lambda v: v >= 0.05),
        ],
        "Leverage": [
            ("D/E Ratio",           ratios.get("de_ratio"),          lambda v: v <= 1.5),
            ("Debt-to-Assets",      ratios.get("debt_to_assets"),    lambda v: v <= 0.5),
            ("Interest Coverage",   ratios.get("interest_coverage"), lambda v: v >= 3.0),
        ],
        "Valuation": [
            ("P/E Ratio",           ratios.get("pe_ratio"),          lambda v: 10 <= v <= 30),
            ("P/B Ratio",           ratios.get("pb_ratio"),          lambda v: v <= 3.0),
            ("P/S Ratio",           ratios.get("ps_ratio"),          lambda v: v <= 5.0),
        ],
        "Growth": [
            ("Revenue Growth",      ratios.get("revenue_growth"),    lambda v: v >= 0.05),
            ("Net Income Growth",   ratios.get("ni_growth"),         lambda v: v >= 0.0),
        ],
    }

    for grp_name, items in groups.items():
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(139, 148, 158)
        pdf.cell(0, 6, f"  -- {grp_name} --", ln=True)
        for label, val, cond in items:
            if val is not None:
                fmt_val = f"{val:.4f}" if isinstance(val, float) else str(val)
                try:
                    good = cond(val)
                except Exception:
                    good = None
                pdf.ratio_row(label, fmt_val, good)
        pdf.ln(2)

    # ── AI Recommendation ──
    pdf.add_page()
    pdf.set_fill_color(13, 17, 23)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.ln(4)
    pdf.section_title("  AI INVESTMENT RECOMMENDATION")
    if ai_recommendation:
        clean = ai_recommendation.replace("**", "").replace("##", "").replace("#", "")
        pdf.body_text(clean)
    else:
        pdf.body_text("No AI recommendation generated.")

    pdf.ln(4)
    pdf.section_title("  SCENARIO FORECAST (BULL / BASE / BEAR)")
    if ai_forecast:
        clean = ai_forecast.replace("**", "").replace("##", "").replace("#", "")
        pdf.body_text(clean)
    else:
        pdf.body_text("No forecast generated.")

    # Footer note
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(139, 148, 158)
    pdf.multi_cell(
        0, 5,
        "DISCLAIMER: This report is generated by AI for informational purposes only and does not constitute "
        "financial advice. Always consult a qualified financial advisor before making investment decisions.",
    )

    return bytes(pdf.output())


# ═══════════════════════════════════════════════════════════════
#  SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════

def init_session():
    defaults = {
        "ai_cache":        {},
        "chat_history":    [],
        "df_main":         None,
        "df_comp":         None,
        "ratios_main":     None,
        "ratios_comp":     None,
        "cols_main":       None,
        "cols_comp":       None,
        "company_name":    "My Company",
        "competitor_name": "Competitor",
        "api_key_valid":   True, # Bypassed for free version!
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session()


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(
        '<div class="logo-text">📊 FinSight AI</div>'
        '<div class="logo-sub">Financial Intelligence Dashboard</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Status Indicators ──
    st.markdown("**🔧 System Status**")
    api_status  = '<span class="status-dot-green"></span> Engine Online'
    data_status = (
        '<span class="status-dot-green"></span> Data Loaded'
        if st.session_state.df_main is not None
        else '<span class="status-dot-yellow"></span> No Data'
    )
    st.markdown(api_status, unsafe_allow_html=True)
    st.markdown(data_status, unsafe_allow_html=True)
    st.markdown("---")

    # ── Primary File Upload ──
    st.markdown("**📂 Upload Financial Data**")
    st.session_state["company_name"] = st.text_input(
        "Company Name", value=st.session_state["company_name"], placeholder="e.g., Apple Inc."
    )
    uploaded_main = st.file_uploader(
        "Primary Company (CSV / Excel)",
        type=["csv", "xlsx", "xls"],
        key="upload_main",
    )
    if uploaded_main:
        df = load_file(uploaded_main)
        if df is not None and not df.equals(st.session_state.get("df_main_raw", pd.DataFrame())):
            st.session_state["df_main"]     = df
            st.session_state["df_main_raw"] = df.copy()
            ratios, cols = compute_ratios(df)
            st.session_state["ratios_main"] = ratios
            st.session_state["cols_main"]   = cols
            # Clear AI cache for fresh analysis
            st.session_state["ai_cache"]    = {}
            st.success(f"✅ Loaded {df.shape[0]} rows × {df.shape[1]} cols")

    st.markdown("---")

    # ── Competitor File Upload ──
    st.markdown("**⚔️ Competitor Analysis (Optional)**")
    st.session_state["competitor_name"] = st.text_input(
        "Competitor Name", value=st.session_state["competitor_name"], placeholder="e.g., Microsoft"
    )
    uploaded_comp = st.file_uploader(
        "Competitor (CSV / Excel)",
        type=["csv", "xlsx", "xls"],
        key="upload_comp",
    )
    if uploaded_comp:
        df2 = load_file(uploaded_comp)
        if df2 is not None:
            st.session_state["df_comp"]     = df2
            ratios2, cols2 = compute_ratios(df2)
            st.session_state["ratios_comp"] = ratios2
            st.session_state["cols_comp"]   = cols2
            st.success(f"✅ Competitor: {df2.shape[0]}R × {df2.shape[1]}C")

    st.markdown("---")

    # ── Cache Controls ──
    if st.button("🗑️ Clear Engine Cache", use_container_width=True):
        st.session_state["ai_cache"] = {}
        st.success("Cache cleared!")

    if st.button("🔄 Reset All", use_container_width=True):
        for key in ["df_main", "df_comp", "ratios_main", "ratios_comp",
                    "cols_main", "cols_comp", "ai_cache", "chat_history"]:
            st.session_state[key] = {} if "cache" in key else ([] if "history" in key else None)
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<div style="color:#8b949e;font-size:0.72rem;text-align:center;">'
        '© 2026 FinSight AI<br>'
        'Not financial advice.</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════
#  MAIN AREA
# ═══════════════════════════════════════════════════════════════

st.markdown(
    '<h1 style="background:linear-gradient(135deg,#58a6ff,#79c0ff);'
    '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
    'background-clip:text;font-size:2rem;font-weight:800;margin-bottom:4px;">'
    '📊 FinSight AI Dashboard</h1>'
    '<p style="color:#8b949e;font-size:0.9rem;margin-top:0;">'
    'Intelligent financial analysis powered by Engine AI · Real-time ratio engine · Scenario forecasting</p>',
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["🏢 Single Company Analysis", "⚔️ Competitor Comparison Mode"])


# ═══════════════════════════════════════════════════════════════
#  TAB 1  -  SINGLE COMPANY ANALYSIS
# ═══════════════════════════════════════════════════════════════

with tab1:

    df     = st.session_state.get("df_main")
    ratios = st.session_state.get("ratios_main")
    cols   = st.session_state.get("cols_main")
    cname  = st.session_state.get("company_name", "Company")

    if df is None:
        st.markdown(
            '<div class="card" style="text-align:center;padding:48px;">'
            '<div style="font-size:3rem;">📁</div>'
            '<h2 style="color:#58a6ff;margin:16px 0 8px;">Upload Your Financial Data</h2>'
            '<p style="color:#8b949e;max-width:480px;margin:0 auto;">'
            "Upload a CSV or Excel file with your company's financial statements "
            "(Income Statement, Balance Sheet, or combined). "
            "The engine will auto-detect columns and compute all ratios instantly.</p>"
            '<div style="margin-top:24px;color:#8b949e;font-size:0.85rem;">'
            "📌 Supported columns: Revenue, Net Income, Total Assets, Total Equity, "
            "Current Assets, Current Liabilities, EPS, Price, and more.</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.stop()

    # ───────────────────────────────────────────
    #  KPI SUMMARY CARDS
    # ───────────────────────────────────────────
    st.markdown('<div class="section-header">📌 Key Performance Indicators</div>', unsafe_allow_html=True)

    rev_col = cols.get("revenue")
    ni_col  = cols.get("net_income")
    yr_col  = cols.get("year")

    def latest_val(col_name):
        if col_name and col_name in df.columns:
            s = pd.to_numeric(df[col_name], errors="coerce").dropna()
            return s.iloc[-1] if len(s) else None
        return None

    def prev_val(col_name):
        if col_name and col_name in df.columns:
            s = pd.to_numeric(df[col_name], errors="coerce").dropna()
            return s.iloc[-2] if len(s) >= 2 else None
        return None

    rev_latest = latest_val(rev_col)
    ni_latest  = latest_val(ni_col)
    rev_prev   = prev_val(rev_col)
    ni_prev    = prev_val(ni_col)

    rev_delta = f"{((rev_latest-rev_prev)/abs(rev_prev)*100):.1f}%" if (rev_latest and rev_prev and rev_prev != 0) else None
    ni_delta  = f"{((ni_latest-ni_prev)/abs(ni_prev)*100):.1f}%"   if (ni_latest  and ni_prev  and ni_prev  != 0) else None

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("💰 Revenue", fmt_large(rev_latest) if rev_latest else "N/A", delta=rev_delta)
    with k2:
        st.metric("📈 Net Income", fmt_large(ni_latest) if ni_latest else "N/A", delta=ni_delta)
    with k3:
        pe = ratios.get("pe_ratio")
        st.metric("📊 P/E Ratio", f"{pe:.1f}x" if pe else "N/A")
    with k4:
        nm = ratios.get("net_margin")
        st.metric("💹 Net Margin", f"{nm*100:.1f}%" if nm else "N/A")
    with k5:
        rs = ratios.get("risk_score", 50)
        risk_label = "🟢 Low" if rs <= 33 else ("🟡 Medium" if rs <= 66 else "🔴 High")
        st.metric("⚠️ Risk", risk_label, delta=f"Score: {rs:.0f}/100", delta_color="off")

    st.markdown("---")

    # ───────────────────────────────────────────
    #  MAIN CHARTS  (Revenue Trend + Net Income)
    # ───────────────────────────────────────────
    if yr_col and rev_col:
        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.markdown('<div class="section-header">📈 Revenue & Income Trends</div>', unsafe_allow_html=True)
            fig_rev = chart_revenue_trend(df, yr_col, rev_col)
            st.plotly_chart(fig_rev, use_container_width=True)

        with col_right:
            if ni_col:
                st.markdown('<div class="section-header">💰 Net Income Trend</div>', unsafe_allow_html=True)
                fig_ni = chart_net_income_trend(df, yr_col, ni_col)
                st.plotly_chart(fig_ni, use_container_width=True)
            else:
                st.warning("Net Income column not detected. Ensure column is named 'Net Income', 'Net Profit', or similar.")
    else:
        st.warning(
            "⚠️ Could not detect Year/Revenue columns. Detected columns: " +
            ", ".join(df.columns.tolist()[:10]) +
            ". Rename columns to 'Year', 'Revenue', etc. for best results."
        )

    # ───────────────────────────────────────────────────────────
    #  GRANULAR DATA DRILL-DOWN  (100% local pandas - zero API)
    # ───────────────────────────────────────────────────────────
    if yr_col:
        st.markdown("---")
        st.markdown(
            '<div class="section-header">🔍 Granular Data Drill-Down</div>',
            unsafe_allow_html=True,
        )

        INCOME_KEYWORDS  = ["revenue", "sales", "income", "profit", "ebit", "ebitda",
                             "margin", "earnings", "turnover", "cogs", "cost of goods",
                             "gross", "operating expense", "tax", "interest expense",
                             "depreciation", "amortization", "r&d", "research"]
        ASSET_KEYWORDS   = ["asset", "cash", "inventory", "receivable", "investment",
                             "property", "equipment", "goodwill", "intangible",
                             "prepaid", "deferred", "ppe", "capex"]
        LIAB_KEYWORDS    = ["liabilit", "debt", "payable", "borrowing", "loan",
                             "obligation", "equity", "capital", "retained", "dividend",
                             "minority", "reserve", "surplus"]

        def classify_col(col_name: str) -> str:
            cl = col_name.lower()
            if any(k in cl for k in INCOME_KEYWORDS):
                return "📊 Income Statement"
            if any(k in cl for k in ASSET_KEYWORDS):
                return "🏦 Assets"
            if any(k in cl for k in LIAB_KEYWORDS):
                return "⚖️ Liabilities & Equity"
            return "📋 Other Metrics"

        year_series = df[yr_col].dropna().astype(str).unique().tolist()
        try:
            year_series_sorted = sorted(year_series, key=lambda x: float(x), reverse=True)
        except ValueError:
            year_series_sorted = sorted(year_series, reverse=True)

        dd_col1, dd_col2 = st.columns([1, 3])
        with dd_col1:
            selected_year = st.selectbox(
                "📅 Select Year to Drill Into",
                options=year_series_sorted,
                index=0,
                key="drilldown_year",
                help="Choose a fiscal year to see the full data breakdown for that period.",
            )

        year_mask  = df[yr_col].astype(str) == str(selected_year)
        year_row   = df[year_mask].copy()

        if year_row.empty:
            st.warning(f"No data found for year **{selected_year}**.")
        else:
            row_data = year_row.iloc[0]

            sel_idx = year_series_sorted.index(str(selected_year))
            prev_year_str = year_series_sorted[sel_idx + 1] if sel_idx + 1 < len(year_series_sorted) else None
            prev_row = None
            if prev_year_str:
                prev_mask = df[yr_col].astype(str) == prev_year_str
                if prev_mask.any():
                    prev_row = df[prev_mask].iloc[0]

            numeric_cols = [
                c for c in df.columns
                if c != yr_col and pd.api.types.is_numeric_dtype(df[c])
            ]

            groups: dict[str, list] = {}
            for c in numeric_cols:
                grp = classify_col(c)
                groups.setdefault(grp, []).append(c)

            GROUP_ORDER = [
                "📊 Income Statement",
                "🏦 Assets",
                "⚖️ Liabilities & Equity",
                "📋 Other Metrics",
            ]

            for grp_name in GROUP_ORDER:
                grp_cols = groups.get(grp_name, [])
                if not grp_cols:
                    continue

                rows = []
                for col_name in grp_cols:
                    val = row_data.get(col_name, None)
                    try:
                        val_num = float(val)
                    except (TypeError, ValueError):
                        val_num = None

                    prev_num = None
                    if prev_row is not None:
                        try:
                            prev_num = float(prev_row.get(col_name, None))
                        except (TypeError, ValueError):
                            prev_num = None

                    yoy_pct = None
                    if val_num is not None and prev_num is not None and prev_num != 0:
                        yoy_pct = (val_num - prev_num) / abs(prev_num) * 100

                    rows.append({
                        "Metric":          col_name,
                        f"{selected_year} Value": fmt_large(val_num) if val_num is not None else "N/A",
                        f"{prev_year_str} Value" if prev_year_str else "Prev Year": fmt_large(prev_num) if prev_num is not None else "—",
                        "YoY Change":      (
                            f"{'▲' if yoy_pct >= 0 else '▼'} {abs(yoy_pct):.1f}%"
                            if yoy_pct is not None else "—"
                        ),
                        "_yoy_raw":        yoy_pct,
                    })

                grp_df = pd.DataFrame(rows)
                display_df = grp_df.drop(columns=["_yoy_raw"])

                st.markdown(
                    f'<div style="color:#8b949e;font-weight:700;font-size:0.82rem;'
                    f'text-transform:uppercase;letter-spacing:0.1em;margin:18px 0 6px;">'
                    f'{grp_name}</div>',
                    unsafe_allow_html=True,
                )

                def _style_row(row):
                    styles = [""] * len(row)
                    yoy_col = "YoY Change"
                    if yoy_col in row.index:
                        raw_idx = list(display_df.columns).index(yoy_col)
                        val_str = row[yoy_col]
                        if isinstance(val_str, str) and "▲" in val_str:
                            styles[raw_idx] = "color: #3fb950; font-weight: 600"
                        elif isinstance(val_str, str) and "▼" in val_str:
                            styles[raw_idx] = "color: #f85149; font-weight: 600"
                    return styles

                styled = (
                    display_df.style
                    .apply(_style_row, axis=1)
                    .set_properties(**{
                        "background-color": "#161b22",
                        "color":            "#e6edf3",
                        "border-color":     "#30363d",
                        "font-size":        "0.85rem",
                    })
                    .set_table_styles([
                        {"selector": "thead th", "props": [
                            ("background-color", "#0d1117"),
                            ("color",            "#58a6ff"),
                            ("font-weight",      "700"),
                            ("font-size",        "0.8rem"),
                            ("text-transform",   "uppercase"),
                            ("border-bottom",    "2px solid #30363d"),
                            ("padding",          "8px 12px"),
                        ]},
                        {"selector": "tbody td", "props": [
                            ("padding",       "6px 12px"),
                            ("border-bottom", "1px solid #21262d"),
                        ]},
                        {"selector": "tbody tr:hover td", "props": [
                            ("background-color", "#1c2128"),
                        ]},
                    ])
                    .hide(axis="index")
                )
                st.dataframe(display_df, use_container_width=True, hide_index=True)

            st.markdown(
                f'<div style="margin-top:24px;margin-bottom:10px;">'
                f'<span style="color:#58a6ff;font-weight:700;font-size:0.95rem;">'
                f'📐 Year-over-Year Growth KPIs — {selected_year}'
                + (f' vs {prev_year_str}' if prev_year_str else '')
                + '</span></div>',
                unsafe_allow_html=True,
            )

            if prev_row is None:
                st.info(
                    f"ℹ️ No prior year data available before **{selected_year}** to compute YoY growth. "
                    "Select a later year to see comparisons."
                )
            else:
                kpi_items = []
                for col_name in numeric_cols:
                    try:
                        cur  = float(row_data.get(col_name, None))
                        prev = float(prev_row.get(col_name, None))
                        if not (math.isnan(cur) or math.isnan(prev)) and prev != 0:
                            pct = (cur - prev) / abs(prev) * 100
                            kpi_items.append((col_name, cur, prev, pct))
                    except (TypeError, ValueError):
                        continue

                if not kpi_items:
                    st.warning("No numeric columns with prior-year data found for YoY comparison.")
                else:
                    pinned_keys   = [rev_col, ni_col]
                    pinned_items  = [k for k in kpi_items if k[0] in pinned_keys and k[0] is not None]
                    other_items   = [k for k in kpi_items if k[0] not in pinned_keys]

                    if pinned_items:
                        pcols = st.columns(len(pinned_items))
                        for i, (col_name, cur, prev, pct) in enumerate(pinned_items):
                            arrow  = "▲" if pct >= 0 else "▼"
                            color  = "#3fb950" if pct >= 0 else "#f85149"
                            with pcols[i]:
                                st.markdown(
                                    f'<div style="background:linear-gradient(135deg,#161b22,#1c2128);'
                                    f'border:1px solid #30363d;border-radius:12px;padding:18px 22px;'
                                    f'border-left:4px solid {color};">'
                                    f'<div style="color:#8b949e;font-size:0.75rem;text-transform:uppercase;'
                                    f'letter-spacing:0.08em;margin-bottom:6px;">{col_name}</div>'
                                    f'<div style="color:#e6edf3;font-size:1.5rem;font-weight:700;'
                                    f'margin-bottom:4px;">{fmt_large(cur)}</div>'
                                    f'<div style="color:{color};font-size:0.9rem;font-weight:600;">'
                                    f'{arrow} {abs(pct):.1f}% vs {prev_year_str}</div>'
                                    f'<div style="color:#8b949e;font-size:0.78rem;margin-top:2px;">'
                                    f'Prior: {fmt_large(prev)}</div>'
                                    f'</div>',
                                    unsafe_allow_html=True,
                                )

                    if other_items:
                        st.markdown(
                            '<div style="color:#8b949e;font-size:0.78rem;'
                            'margin:16px 0 8px;text-transform:uppercase;letter-spacing:0.08em;">'
                            'All Other Metrics</div>',
                            unsafe_allow_html=True,
                        )
                        n_cols = 4
                        for row_start in range(0, len(other_items), n_cols):
                            chunk = other_items[row_start: row_start + n_cols]
                            grid  = st.columns(n_cols)
                            for j, (col_name, cur, prev, pct) in enumerate(chunk):
                                arrow = "▲" if pct >= 0 else "▼"
                                color = "#3fb950" if pct >= 0 else "#f85149"
                                with grid[j]:
                                    st.metric(
                                        label=col_name,
                                        value=fmt_large(cur),
                                        delta=f"{arrow} {abs(pct):.1f}%",
                                        delta_color="normal" if pct >= 0 else "inverse",
                                    )

    # ───────────────────────────────────────────
    #  YoY GROWTH + RADAR
    # ───────────────────────────────────────────
    if yr_col:
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown('<div class="section-header">📊 Year-over-Year Growth</div>', unsafe_allow_html=True)
            growth_cols = [
                ("Revenue",    cols.get("revenue")),
                ("Net Income", cols.get("net_income")),
                ("Total Assets", cols.get("total_assets")),
            ]
            fig_yoy = chart_yoy_growth(df, yr_col, growth_cols)
            if fig_yoy:
                st.plotly_chart(fig_yoy, use_container_width=True)
            else:
                st.info("Not enough data for YoY growth chart.")

        with c_right:
            st.markdown('<div class="section-header">🕸️ Financial Health Radar</div>', unsafe_allow_html=True)
            fig_radar = chart_ratio_radar(ratios)
            if fig_radar:
                st.plotly_chart(fig_radar, use_container_width=True)
            else:
                st.info("Not enough ratio data for radar chart.")

    st.markdown("---")

    # ───────────────────────────────────────────
    #  RATIO METRIC PANELS  (4 groups)
    # ───────────────────────────────────────────
    st.markdown('<div class="section-header">🔢 Financial Ratio Engine</div>', unsafe_allow_html=True)

    def ratio_metric(col, label, value, fmt=".2f", good_thresh=None, direction="high"):
        with col:
            if value is not None:
                formatted = f"{value:{fmt}}"
                if good_thresh is not None:
                    good = value >= good_thresh if direction == "high" else value <= good_thresh
                    delta_str = "✅ Healthy" if good else "⚠️ Watch"
                    delta_color = "normal" if good else "inverse"
                else:
                    delta_str, delta_color = None, "off"
                st.metric(label, formatted, delta=delta_str, delta_color=delta_color)
            else:
                st.metric(label, "N/A")

    rg1, rg2, rg3, rg4 = st.columns(4)

    with rg1:
        st.markdown('<div style="color:#58a6ff;font-weight:700;font-size:0.9rem;margin-bottom:8px;">💧 Liquidity</div>', unsafe_allow_html=True)
        ratio_metric(rg1, "Current Ratio",   ratios.get("current_ratio"),  ".2f", 1.5)
        ratio_metric(rg1, "Quick Ratio",     ratios.get("quick_ratio"),    ".2f", 1.0)
        ratio_metric(rg1, "Cash Ratio",      ratios.get("cash_ratio"),     ".2f", 0.5)

    with rg2:
        st.markdown('<div style="color:#3fb950;font-weight:700;font-size:0.9rem;margin-bottom:8px;">📈 Profitability</div>', unsafe_allow_html=True)
        nm_pct = ratios.get("net_margin")
        gm_pct = ratios.get("gross_margin")
        ratio_metric(rg2, "Net Margin",   nm_pct,           ".2%", 0.10)
        ratio_metric(rg2, "Gross Margin", gm_pct,           ".2%", 0.30)
        ratio_metric(rg2, "ROE",          ratios.get("roe"), ".2%", 0.10)
        ratio_metric(rg2, "ROA",          ratios.get("roa"), ".2%", 0.05)

    with rg3:
        st.markdown('<div style="color:#f85149;font-weight:700;font-size:0.9rem;margin-bottom:8px;">⚖️ Leverage</div>', unsafe_allow_html=True)
        ratio_metric(rg3, "D/E Ratio",          ratios.get("de_ratio"),          ".2f", 1.5, "low")
        ratio_metric(rg3, "Debt-to-Assets",     ratios.get("debt_to_assets"),    ".2f", 0.5, "low")
        ratio_metric(rg3, "Interest Coverage",  ratios.get("interest_coverage"), ".1f", 3.0)

    with rg4:
        st.markdown('<div style="color:#d29922;font-weight:700;font-size:0.9rem;margin-bottom:8px;">💎 Valuation</div>', unsafe_allow_html=True)
        ratio_metric(rg4, "P/E Ratio", ratios.get("pe_ratio"), ".1f")
        ratio_metric(rg4, "P/B Ratio", ratios.get("pb_ratio"), ".2f")
        ratio_metric(rg4, "P/S Ratio", ratios.get("ps_ratio"), ".2f")
        rev_g = ratios.get("revenue_growth")
        st.metric("Revenue Growth", f"{rev_g*100:.1f}%" if rev_g is not None else "N/A")

    st.markdown("---")

    # ───────────────────────────────────────────
    #  RISK GAUGE + AI RECOMMENDATION
    # ───────────────────────────────────────────
    gauge_col, rec_col = st.columns([1, 2])

    with gauge_col:
        st.markdown('<div class="section-header">⚠️ Risk Score Meter</div>', unsafe_allow_html=True)
        rs = ratios.get("risk_score", 50)
        st.plotly_chart(chart_risk_gauge(rs), use_container_width=True)

        with st.expander("📖 How is risk calculated?"):
            st.markdown("""
**Risk score components:**
- 🔵 Current Ratio contribution (Liquidity)
- 🔴 D/E Ratio contribution (Leverage)
- 🟢 Net Margin contribution (Profitability)
- 🟢 ROE contribution (Returns)
- 🟡 Revenue Growth (Momentum)

Score range: **0 (safest) → 100 (highest risk)**
""")

    with rec_col:
        st.markdown('<div class="section-header">🤖 AI Investment Card</div>', unsafe_allow_html=True)

        cache_key = f"{cname}_{hash(str(ratios))}"
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            gen_rec = st.button("🤖 Generate AI Recommendation", key="btn_rec", use_container_width=True)
        with col_btn2:
            clear_rec = st.button("🗑️ Clear Recommendation", key="btn_clear_rec", use_container_width=True)

        if clear_rec:
            st.session_state["ai_cache"].pop(cache_key, None)

        if gen_rec or cache_key in st.session_state.get("ai_cache", {}):
            with st.spinner("🧠 AI is analyzing your financials..."):
                rec_text = get_ai_recommendation(ratios, cname, cache_key)

            rec_upper = rec_text.upper()
            if "BUY" in rec_upper[:200]:
                badge = '<span class="rec-badge-buy">📈 BUY</span>'
            elif "SELL" in rec_upper[:200]:
                badge = '<span class="rec-badge-sell">📉 SELL</span>'
            else:
                badge = '<span class="rec-badge-hold">⏸️ HOLD</span>'

            st.markdown(
                f'<div class="ai-card">'
                f'<div style="margin-bottom:14px;">{badge}</div>'
                f'<div style="color:#cdd9e5;font-size:0.88rem;line-height:1.7;">'
                f'{rec_text.replace(chr(10), "<br>")}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ───────────────────────────────────────────
    #  SCENARIO FORECASTING
    # ───────────────────────────────────────────
    st.markdown('<div class="section-header">🔮 AI Scenario Forecast (Bull / Base / Bear)</div>', unsafe_allow_html=True)

    fc_cache_key = f"{cname}_fc_{hash(str(ratios))}"
    fc_col1, fc_col2 = st.columns([1, 5])
    with fc_col1:
        gen_fc = st.button("🔮 Generate Forecast", key="btn_fc", use_container_width=True)

    if gen_fc or (fc_cache_key + "_forecast") in st.session_state.get("ai_cache", {}):
        with st.spinner("🧠 Building Bull / Base / Bear scenarios..."):
            fc_text = get_ai_forecast(df, ratios, cname, fc_cache_key)

        lines = fc_text.split("\n")
        bull_lines, base_lines, bear_lines, other_lines = [], [], [], []
        current_section = "other"

        for line in lines:
            lu = line.upper()
            if "BULL" in lu:
                current_section = "bull"
            elif "BASE" in lu:
                current_section = "base"
            elif "BEAR" in lu:
                current_section = "bear"

            if current_section == "bull":
                bull_lines.append(line)
            elif current_section == "base":
                base_lines.append(line)
            elif current_section == "bear":
                bear_lines.append(line)
            else:
                other_lines.append(line)

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            bull_html = "<br>".join(bull_lines) if bull_lines else fc_text.replace("\n", "<br>")
            st.markdown(
                f'<div class="scenario-bull">'
                f'<div style="color:#3fb950;font-weight:700;font-size:1rem;margin-bottom:8px;">🐂 Bull Case</div>'
                f'<div style="color:#cdd9e5;font-size:0.84rem;line-height:1.7;">{bull_html}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
        with sc2:
            base_html = "<br>".join(base_lines) if base_lines else ""
            st.markdown(
                f'<div class="scenario-base">'
                f'<div style="color:#58a6ff;font-weight:700;font-size:1rem;margin-bottom:8px;">📊 Base Case</div>'
                f'<div style="color:#cdd9e5;font-size:0.84rem;line-height:1.7;">{base_html}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
        with sc3:
            bear_html = "<br>".join(bear_lines) if bear_lines else ""
            st.markdown(
                f'<div class="scenario-bear">'
                f'<div style="color:#f85149;font-weight:700;font-size:1rem;margin-bottom:8px;">🐻 Bear Case</div>'
                f'<div style="color:#cdd9e5;font-size:0.84rem;line-height:1.7;">{bear_html}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

        if other_lines:
            st.markdown(
                f'<div class="card" style="margin-top:12px;">'
                f'<div style="color:#8b949e;font-size:0.85rem;line-height:1.7;">'
                + "<br>".join(other_lines) +
                f"</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ───────────────────────────────────────────
    #  RAW DATA & DOWNLOAD SECTION
    # ───────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Raw Data & Export</div>', unsafe_allow_html=True)

    with st.expander("🔍 View Loaded Dataset", expanded=False):
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )
        csv_bytes = df.to_csv(index=False).encode()
        st.download_button(
            "⬇️ Download CSV",
            data=csv_bytes,
            file_name=f"{cname}_data.csv",
            mime="text/csv",
        )

    # ── PDF Export ──
    pdf_col1, pdf_col2 = st.columns([2, 3])
    with pdf_col1:
        st.markdown("**📄 Executive Summary PDF**")
        if st.button("📄 Generate & Download PDF Report", key="btn_pdf", use_container_width=True):
            ai_rec  = st.session_state.get("ai_cache", {}).get(f"{cname}_{hash(str(ratios))}")
            ai_fc   = st.session_state.get("ai_cache", {}).get(f"{cname}_fc_{hash(str(ratios))}_forecast")
            with st.spinner("📄 Compiling PDF report..."):
                pdf_bytes = generate_pdf(cname, ratios, ai_rec, ai_fc, df)
            st.download_button(
                "⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=f"{cname}_FinSight_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                key="download_pdf",
            )
            st.success("✅ PDF ready!")

    st.markdown("---")

    # ───────────────────────────────────────────
    #  CFO CHATBOT
    # ───────────────────────────────────────────
    st.markdown('<div class="section-header">💬 Chat with Your Financials (CFO AI)</div>', unsafe_allow_html=True)

    # Render chat history
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user"><b>You:</b> {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-ai"><b>🤖 FinSight AI:</b><br>{msg["content"].replace(chr(10), "<br>")}</div>',
                unsafe_allow_html=True,
            )

    user_question = st.chat_input("Ask anything about your financials... (e.g., 'Is our debt level sustainable?')")
    if user_question:
        st.session_state["chat_history"].append({"role": "user", "content": user_question})

        context_lines = [f"Company: {cname}"]
        for k, v in ratios.items():
            if v is not None:
                fmt = f"{v:.4f}" if isinstance(v, float) else str(v)
                context_lines.append(f"{k}: {fmt}")
        if yr_col and rev_col:
            context_lines.append(f"\nRevenue data (last 5 rows):\n{df[[yr_col, rev_col]].tail(5).to_string(index=False)}")
        context = "\n".join(context_lines)

        with st.spinner("🧠 FinSight AI is thinking..."):
            reply = get_ai_chat_response(user_question, context)
        st.session_state["chat_history"].append({"role": "assistant", "content": reply})
        st.rerun()

    if st.session_state["chat_history"]:
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            st.session_state["chat_history"] = []
            st.rerun()


# ═══════════════════════════════════════════════════════════════
#  TAB 2  -  COMPETITOR COMPARISON MODE
# ═══════════════════════════════════════════════════════════════

with tab2:

    df1     = st.session_state.get("df_main")
    df2     = st.session_state.get("df_comp")
    ratios1 = st.session_state.get("ratios_main")
    ratios2 = st.session_state.get("ratios_comp")
    cols1   = st.session_state.get("cols_main")
    cols2   = st.session_state.get("cols_comp")
    name1   = st.session_state.get("company_name",    "Company A")
    name2   = st.session_state.get("competitor_name", "Company B")

    if df1 is None and df2 is None:
        st.markdown(
            '<div class="card" style="text-align:center;padding:48px;">'
            '<div style="font-size:3rem;">⚔️</div>'
            '<h2 style="color:#58a6ff;margin:16px 0 8px;">Competitor Comparison Mode</h2>'
            '<p style="color:#8b949e;max-width:520px;margin:0 auto;">'
            "Upload both a primary company file and a competitor file in the sidebar "
            "to unlock side-by-side financial comparison powered by Engine AI.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    elif df1 is None:
        st.warning("⚠️ Please upload the primary company file in the sidebar first.")
    elif df2 is None:
        st.warning("⚠️ Please upload the competitor file in the sidebar to enable comparison mode.")
    else:
        st.markdown(
            f'<h2 style="color:#e6edf3;font-size:1.4rem;font-weight:700;margin-bottom:4px;">'
            f'⚔️ {name1} <span style="color:#8b949e;">vs</span> {name2}</h2>'
            f'<p style="color:#8b949e;font-size:0.85rem;">Head-to-head financial comparison · AI investment verdict</p>',
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # ── Side-by-side KPI comparison ──
        st.markdown('<div class="section-header">📌 KPI Head-to-Head</div>', unsafe_allow_html=True)

        kpi_labels = [
            ("Revenue Growth",   "revenue_growth",   "{:.1%}"),
            ("Net Margin",       "net_margin",        "{:.1%}"),
            ("ROE",              "roe",               "{:.1%}"),
            ("ROA",              "roa",               "{:.1%}"),
            ("Current Ratio",    "current_ratio",     "{:.2f}"),
            ("D/E Ratio",        "de_ratio",          "{:.2f}"),
            ("P/E Ratio",        "pe_ratio",          "{:.1f}x"),
            ("Risk Score",       "risk_score",        "{:.0f}/100"),
        ]

        col_lbl, col_a, col_b = st.columns([2, 1, 1])
        col_lbl.markdown(f'<div style="color:#8b949e;font-weight:600;font-size:0.8rem;">METRIC</div>', unsafe_allow_html=True)
        col_a.markdown(f'<div style="color:#58a6ff;font-weight:700;font-size:0.85rem;">{name1}</div>', unsafe_allow_html=True)
        col_b.markdown(f'<div style="color:#3fb950;font-weight:700;font-size:0.85rem;">{name2}</div>', unsafe_allow_html=True)

        for label, key, fmt in kpi_labels:
            v1 = ratios1.get(key) if ratios1 else None
            v2 = ratios2.get(key) if ratios2 else None

            col_lbl, col_a, col_b = st.columns([2, 1, 1])
            col_lbl.markdown(f'<div style="color:#8b949e;font-size:0.85rem;padding:4px 0;">{label}</div>', unsafe_allow_html=True)

            def fmt_v(v, fmt_str):
                if v is None:
                    return "N/A"
                try:
                    return fmt_str.format(v)
                except Exception:
                    return str(v)

            if v1 is not None and v2 is not None:
                better_high = key not in ("de_ratio", "risk_score", "debt_to_assets")
                a_wins = (v1 > v2) if better_high else (v1 < v2)
                a_color = "#58a6ff" if a_wins else "#8b949e"
                b_color = "#3fb950" if not a_wins else "#8b949e"
                a_badge = " ✅" if a_wins else ""
                b_badge = " ✅" if not a_wins else ""
            else:
                a_color, b_color = "#8b949e", "#8b949e"
                a_badge, b_badge = "", ""

            col_a.markdown(f'<div style="color:{a_color};font-weight:600;font-size:0.88rem;padding:4px 0;">{fmt_v(v1, fmt)}{a_badge}</div>', unsafe_allow_html=True)
            col_b.markdown(f'<div style="color:{b_color};font-weight:600;font-size:0.88rem;padding:4px 0;">{fmt_v(v2, fmt)}{b_badge}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # ── Revenue Comparison Chart ──
        yr1 = cols1.get("year") if cols1 else None
        yr2 = cols2.get("year") if cols2 else None
        rv1 = cols1.get("revenue") if cols1 else None
        rv2 = cols2.get("revenue") if cols2 else None

        if rv1 and rv2:
            st.markdown('<div class="section-header">📊 Revenue Comparison Chart</div>', unsafe_allow_html=True)
            fig_comp = chart_competitor_grouped(df1, df2, yr1, yr2, rv1, rv2, name1, name2)
            st.plotly_chart(fig_comp, use_container_width=True)

        # ── Radar overlay comparison ──
        if ratios1 and ratios2:
            st.markdown('<div class="section-header">🕸️ Financial Health Radar – Overlay</div>', unsafe_allow_html=True)

            mapping = {
                "Current Ratio": ("current_ratio", 3),
                "ROE (×10)":     ("roe",            10),
                "ROA (×10)":     ("roa",            10),
                "Net Margin":    ("net_margin",      100),
                "Gross Margin":  ("gross_margin",    100),
            }
            cats = list(mapping.keys()) + [list(mapping.keys())[0]]
            vals_a = [min(10, max(0, (ratios1.get(k, 0) or 0) * m)) for _, (k, m) in mapping.items()]
            vals_b = [min(10, max(0, (ratios2.get(k, 0) or 0) * m)) for _, (k, m) in mapping.items()]
            vals_a += [vals_a[0]]
            vals_b += [vals_b[0]]

            fig_overlay = go.Figure()
            fig_overlay.add_trace(go.Scatterpolar(r=vals_a, theta=cats, fill="toself",
                                                   fillcolor="rgba(88,166,255,0.15)", line=dict(color="#58a6ff", width=2),
                                                   marker=dict(size=6), name=name1))
            fig_overlay.add_trace(go.Scatterpolar(r=vals_b, theta=cats, fill="toself",
                                                   fillcolor="rgba(63,185,80,0.12)", line=dict(color="#3fb950", width=2),
                                                   marker=dict(size=6), name=name2))
            fig_overlay.update_layout(
                polar=dict(
                    bgcolor="rgba(22,27,34,0.5)",
                    radialaxis=dict(visible=True, range=[0, 10], gridcolor="#21262d"),
                    angularaxis=dict(gridcolor="#21262d", tickfont=dict(color="#8b949e")),
                ),
                height=350, **PLOTLY_LAYOUT,
            )
            st.plotly_chart(fig_overlay, use_container_width=True)

        st.markdown("---")

        # ── AI Verdict ──
        st.markdown('<div class="section-header">🤖 AI Investment Verdict</div>', unsafe_allow_html=True)

        vkey = f"verdict_{name1}_{name2}"
        if st.button("🤖 Get AI Investment Verdict", key="btn_verdict", use_container_width=False):
            pass

        if st.button("Get Verdict", key="btn_verdict2") or (vkey + "_comp") in st.session_state.get("ai_cache", {}):
            with st.spinner(f"🧠 AI is comparing {name1} vs {name2}..."):
                verdict = get_ai_competitor_verdict(name1, ratios1, name2, ratios2, vkey)
            st.markdown(
                f'<div class="ai-card">'
                f'<div style="color:#d29922;font-weight:700;font-size:1rem;margin-bottom:12px;">⚔️ AI Competitive Analysis: {name1} vs {name2}</div>'
                f'<div style="color:#cdd9e5;font-size:0.88rem;line-height:1.75;">'
                f'{verdict.replace(chr(10), "<br>")}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

        comp_cache_key = vkey
        btn_verdict_main = st.button("⚔️ Generate Full Comparison Report", key="btn_comp_main", use_container_width=True)
        if btn_verdict_main:
            with st.spinner(f"🧠 Generating comparison report..."):
                verdict = get_ai_competitor_verdict(name1, ratios1, name2, ratios2, comp_cache_key)
            st.markdown(
                f'<div class="ai-card">'
                f'<div style="color:#d29922;font-weight:700;font-size:1.1rem;margin-bottom:14px;">🏆 Investment Winner Analysis</div>'
                f'<div style="color:#cdd9e5;font-size:0.88rem;line-height:1.8;">'
                f'{verdict.replace(chr(10), "<br>")}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # ── Comparative PDF export ──
        st.markdown("**📄 Comparison PDF Report**")

        if st.button("📊 Generate Comparison PDF", key="btn_comp_pdf", use_container_width=False):
            verdict_cached = st.session_state.get("ai_cache", {}).get(f"verdict_{name1}_{name2}_comp", "")
            with st.spinner("Compiling comparison PDF..."):
                # FIX 1: Changed the smart en-dash (–) to a standard hyphen (-) to prevent FPDF encoding errors
                combined_ratios = {
                    **{f"{name1} - {k}": v for k, v in ratios1.items()},
                    **{f"{name2} - {k}": v for k, v in ratios2.items()},
                }
                # Generate and save bytes safely to session state
                st.session_state["comp_pdf_bytes"] = generate_pdf(
                    f"{name1} vs {name2}",
                    combined_ratios,
                    verdict_cached,
                    "",
                )
            st.success("🎉 PDF compiled successfully! Ready for download below.")

        # FIX 2: Rendered outside the conditional block so it stays visible during the download execution
        if "comp_pdf_bytes" in st.session_state:
            st.download_button(
                label="⬇️ Download Comparison PDF",
                data=st.session_state["comp_pdf_bytes"],
                file_name=f"Comparison_{name1}_vs_{name2}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                key="download_comp_pdf"
            ) 
