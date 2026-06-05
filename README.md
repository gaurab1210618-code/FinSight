# 📊 FinSight
### Financial Analysis & Investment Advisor

> Intelligent financial analysis powered by a real-time ratio engine · Scenario forecasting · Competitor comparison

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🚀 Overview

**FinSight** is a production-ready Streamlit dashboard that lets students and analysts upload company financial statements and instantly receive deep financial intelligence — no spreadsheet expertise required.

Upload a CSV or Excel file of a company's financials and FinSight will:

- ⚡ Automatically detect and parse financial columns
- 📐 Compute 20+ standard financial ratios across five categories
- 🤖 Generate AI-powered investment recommendations (BUY / HOLD / SELL)
- 📈 Predict Bull, Base, and Bear case scenario forecasts
- ⚔️ Run side-by-side competitor comparisons with an AI verdict
- 📄 Export polished PDF reports ready for presentation

---

## ✨ Features

### 📌 Key Performance Indicators
Displays live KPI cards for Revenue, Net Income, P/E Ratio, Net Margin, and Risk Score — each with YoY delta indicators.

### 📐 Ratio Engine (Pure Python — No External API)
Dynamically detects financial columns and computes ratios across five categories:

| Category | Ratios |
|---|---|
| **Liquidity** | Current Ratio, Quick Ratio, Cash Ratio |
| **Profitability** | Gross Margin, Net Margin, EBIT Margin, ROE, ROA |
| **Leverage** | D/E Ratio, Debt-to-Assets, Interest Coverage |
| **Valuation** | P/E Ratio, P/B Ratio, P/S Ratio |
| **Growth** | Revenue Growth (YoY), Net Income Growth (YoY) |

### 📊 Interactive Charts
- Revenue & Income Trend (line chart)
- YoY Growth comparison (grouped bar chart)
- Financial Health Radar (spider chart)
- Risk Score Gauge (0–100 scale, color-coded)

### 🤖 AI Investment Advisor
Generates structured investment recommendations with:
- BUY / HOLD / SELL verdict based on multi-factor ratio analysis
- Risk rating (Low / Medium / High)
- Key strengths and risk factors
- Target price range projection
- Investment thesis narrative

### 📈 Scenario Forecasting
Three-scenario outlook with confidence levels:
- 🐂 **Bull Case** — Optimistic growth trajectory
- 📊 **Base Case** — Steady historical-average growth
- 🐻 **Bear Case** — Downside risk scenario

### ⚔️ Competitor Comparison Mode
Upload a second company file to unlock:
- Head-to-head KPI table with winner highlights
- Side-by-side revenue comparison chart
- Overlaid Financial Health Radar for both companies
- AI-generated competitive verdict and investment recommendation

### 💬 CFO Chatbot
Ask financial questions about the uploaded data and get context-aware responses.

### 📄 PDF Export
Download a professional, dark-themed investment report including all ratios, the AI recommendation, scenario forecasts, and an executive summary — for both single-company and competitor comparison analyses.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io/) | Web app framework |
| [Pandas](https://pandas.pydata.org/) | Data loading & manipulation |
| [NumPy](https://numpy.org/) | Numerical computation |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [FPDF2](https://pyfpdf.github.io/fpdf2/) | PDF report generation |

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/gaurab1210618-code/FinSight.git
cd FinSight
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
FinSight/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── sample_data.csv           # Sample financial dataset to try
├── company_a_technova.csv    # Demo dataset – Technova
├── company_b_alphacore.csv   # Demo dataset – Alphacore
└── README.md
```

---

## 📋 Data Format

FinSight accepts **CSV or Excel (.xlsx)** files. Columns are auto-detected — common naming conventions work out of the box.

**Minimum recommended columns:**

| Column | Accepted Names |
|---|---|
| Year / Period | `year`, `fiscal year`, `fy`, `period`, `date` |
| Revenue | `revenue`, `total revenue`, `net revenue`, `sales` |
| Net Income | `net income`, `net profit`, `profit after tax`, `earnings` |
| Total Assets | `total assets`, `assets` |
| Total Equity | `total equity`, `shareholders equity`, `equity` |
| Current Assets | `current assets` |
| Current Liabilities | `current liabilities` |

> The more columns you include, the more ratios and insights FinSight can generate. See `sample_data.csv` for a full example.

---

## 🖥️ Usage

1. **Upload your file** — Use the sidebar to upload a CSV or Excel financial statement.
2. **Enter company name** — Label the company for reports and charts.
3. **Explore the dashboard** — View KPIs, charts, ratios, and AI insights in the **Single Company Analysis** tab.
4. **Compare competitors** *(optional)* — Upload a second file to activate **Competitor Comparison Mode**.
5. **Export** — Click **Generate PDF** to download a shareable investment report.

---

## ⚠️ Disclaimer

> FinSight is built for **educational and informational purposes only**.
> It does not constitute financial advice. Always consult a qualified financial professional before making investment decisions.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ · © 2026 FinSight AI · Not financial advice.</p>
