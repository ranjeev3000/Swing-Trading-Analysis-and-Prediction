**Swing Trading Analysis & Prediction System**

🚀 **Live App:**  
👉 https://swing-trading-and-analysis.streamlit.app/

AlphaSwing is an end-to-end **swing trading analysis platform** built using Python and Streamlit.  
It scans NIFTY 200 stocks, evaluates overall market health, identifies high-probability trade setups, and generates **fully risk-managed trade plans**.

---

## 🌐 Live Application

The project is deployed and publicly accessible here:

🔗 **https://swing-trading-and-analysis.streamlit.app/**

The app allows users to:
- Sync market data
- Run technical scans
- Generate trade plans
- Track pending and active trades
- Assess market breadth in real time

---

## 🚀 Key Features

- 📊 **Market Breadth Analysis** (NIFTY 200 trend participation)
- 🔍 **Rule-Based Technical Screener**
- 📉 **Pullback Swing Trading Strategy**
- 💰 **Automated Position Sizing & Risk Control**
- 📦 **Pending & Active Trade Tracking**
- 🖥 **Interactive Streamlit Dashboard**
- ⚡ End-to-end workflow:  
  **Download → Clean → Screen → Plan → Track**

---

## 🧠 Trading Philosophy

> *Trade strong stocks in strong markets with controlled risk.*

AlphaSwing is designed around professional trading principles:
- Trade **with the trend**
- Buy **pullbacks**, not breakouts
- Always define **risk before reward**
- Preserve capital first, profits second

---

## 📈 Stock Selection Criteria

A stock qualifies **only if all the following conditions are met**:

### 1️⃣ Market Health (Breadth Context)
- Market Breadth = % of stocks trading above 200 EMA
- Used as a **contextual filter**

| Breadth % | Market Condition |
|---------|------------------|
| < 40% | Weak market |
| 40–60% | Neutral |
| > 60% | Strong market |

---

### 2️⃣ Trend Confirmation
- **Price > EMA 200**
- **Price > EMA 50**

Ensures alignment with long-term and medium-term trends.

---

### 3️⃣ Momentum Pullback (RSI)
- **RSI between 30 and 50**

Targets controlled pullbacks within strong uptrends.

---

### 4️⃣ Volume Confirmation
- **3-day average volume > 20-day average volume**

Confirms participation and accumulation.

---

### 5️⃣ ATR-Based Risk Management
- **Stop Loss:** `Price − (1.5 × ATR)`
- **Target:** `Price + (3.0 × ATR)`

Provides a minimum **1:2 risk–reward structure**.

---

### 6️⃣ Risk–Reward Filter
- Trades must satisfy **Risk:Reward ≥ 1:1.5**
- Low-expectancy trades are discarded automatically

---

## 💰 Position Sizing Logic

- **Trading Capital:** User-defined (default ₹2000)
- **Maximum Risk per Trade:** ₹100
- **MTF Buying Power:** 4× leverage

Quantity is calculated using:
- Maximum acceptable loss
- Available buying power  

The **minimum of both** is selected to protect capital.

---

## ⏳ Estimated Holding Period

Each trade includes a realistic holding estimate:

| Condition | Hold Period |
|--------|-------------|
| Volume surge > 2× | 3–7 days (Fast move) |
| RSI < 35 | 10–15 days (Recovery) |
| Otherwise | 5–10 days (Standard swing) |

---

## 🖥 Application Interface

### 🔍 Scanner
- Runs technical scan on NIFTY 200 stocks
- Displays market breadth
- Generates optimized trade setups

### 📦 Pending Orders
- Stores shortlisted trades
- Prevents duplicate entries

### 📊 Active Portfolio
- Tracks open positions
- Supports manual exit management

---

## 📂 Project Structure
<img width="663" height="367" alt="image" src="https://github.com/user-attachments/assets/ed93c9f9-179a-4ad4-9f6a-c3b2e461f374" />



---

## ⚙️ Tech Stack

- Python
- Streamlit
- Pandas & NumPy
- pandas-ta
- yfinance
- Plotly
- scikit-learn

---

## ☁️ Deployment

The application is deployed on **Streamlit Community Cloud**.

🔗 **Live URL:**  
https://swing-trading-and-analysis.streamlit.app/

No local Git installation required for deployment.

---

## ⚠️ Notes & Limitations

- Streamlit Cloud uses **ephemeral storage**
- CSV-based trade logs reset on app restart
- Designed for **educational and research purposes**
- Not intended as financial advice

---

## 🧑‍💻 Author

**Ranjeev**  
Swing Trading | Quant Research | Data Engineer | Python  
GitHub: https://github.com/ranjeev3000

---

## 📌 Disclaimer

This project is for **educational purposes only**.  
Trading in financial markets involves risk. Always do your own research.

---

⭐ If you find this project useful, consider giving the repository a star!
