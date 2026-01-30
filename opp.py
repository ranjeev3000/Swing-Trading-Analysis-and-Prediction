import streamlit as st
import pandas as pd
import os
import datetime

# Internal Modules
from nifty_200 import download_and_map_nifty_200
from bulk_download import bulk_download_data
from screener import screen_stocks
from trade_planner import generate_trade_report

# --- CONSTANTS & PATHS ---
PATHS = {
    "data": "data",
    "screener": "screener",
    "index": "nifty_200_indexed.csv",
    "pending": "screener/pending_trades.csv",
    "active": "screener/active_trades.csv"
}

st.set_page_config(page_title="AlphaSwing Terminal v1.0", layout="wide", page_icon="⚡")

# --- 1. ROBUST INITIALIZATION ---
def init_app():
    for folder in ["data", "screener"]:
        if not os.path.exists(folder): os.makedirs(folder)
    
    # Standardized columns for consistency across all modules
    cols = ["Date", "Stock", "Entry", "Qty", "StopLoss", "Target", "R:R", "Capital_Needed", "Max_Risk", "Status"]
    for file_path in [PATHS["pending"], PATHS["active"]]:
        if not os.path.exists(file_path):
            pd.DataFrame(columns=cols).to_csv(file_path, index=False)

init_app()

# --- 2. DATA FRESHNESS CHECK ---
def get_data_status():
    if not os.path.exists(PATHS["data"]) or not os.listdir(PATHS["data"]):
        return "❌ Missing", "red"
    files = [f for f in os.listdir(PATHS["data"]) if f.endswith('.csv')]
    if not files: return "❌ Missing", "red"
    
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(PATHS["data"], files[0])))
    if mtime.date() == datetime.date.today():
        return f"✅ Fresh ({mtime.strftime('%H:%M')})", "green"
    return f"⚠️ Stale ({mtime.strftime('%Y-%m-%d')})", "orange"

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.title("⚡ AlphaControl")
status_text, status_color = get_data_status()
st.sidebar.markdown(f"Data Status: :{status_color}[{status_text}]")

if st.sidebar.button("🔄 SYNC MARKET DATA", use_container_width=True):
    with st.status("Updating System...", expanded=True) as status:
        st.write("Fetching Nifty 200 constituents...")
        download_and_map_nifty_200()
        st.write("Downloading YFinance Price Action...")
        bulk_download_data(PATHS["index"], PATHS["data"])
        status.update(label="System Synced!", state="complete", expanded=False)
    st.rerun()

st.sidebar.divider()
st.sidebar.subheader("💰 Strategy Risk")
cap = st.sidebar.number_input("Trading Capital", 1000, 100000, 2000)
risk = st.sidebar.slider("Risk Per Trade", 20, 1000, 100)

# --- 4. MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["🔍 SCANNER", "📦 PENDING ORDERS", "📊 ACTIVE PORTFOLIO"])

# --- TAB 1: SCANNER & REACTIVE PLANNER ---
with tab1:
    if st.button("🔎 Run Technical Scan", type="primary"):
        with st.spinner("Analyzing 200+ Charts..."):
            df, breadth = screen_stocks(PATHS["data"])
            st.session_state['scan_results'] = df
            st.session_state['breadth'] = breadth

    if 'scan_results' in st.session_state:
        st.metric("Market Breadth (>EMA 200)", f"{st.session_state['breadth']:.1f}%")
        
        # Live Planner Integration
        plans = generate_trade_report(st.session_state['scan_results'], cap, risk)
        
        if not plans.empty:
            st.subheader("Actionable Setups")
            st.dataframe(plans, use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                selected = st.selectbox("Pick Stock", plans['Stock'])
                url = f"https://www.tradingview.com/chart/?symbol=NSE:{selected}"
                st.link_button(f"🔗 Open {selected} Chart", url)
            
            with col2:
                st.write("###")
                if st.button("📌 Move to Pending", use_container_width=True):
                    row = plans[plans['Stock'] == selected].iloc[0].to_dict()
                    row['Date'] = datetime.date.today().strftime("%Y-%m-%d")
                    row['Status'] = "Pending"
                    
                    pending = pd.read_csv(PATHS["pending"])
                    if selected not in pending['Stock'].values:
                        pd.concat([pending, pd.DataFrame([row])], ignore_index=True).to_csv(PATHS["pending"], index=False)
                        st.toast(f"{selected} Added!")
                    else:
                        st.error("Already in Pending!")
        else:
            st.warning("No stocks found matching your criteria.")

# --- TAB 2: PENDING ORDERS ---
with tab2:
    pending_df = pd.read_csv(PATHS["pending"])
    if not pending_df.empty:
        st.write("Execute these on your broker (Groww/Zerodha/Kite)")
        st.table(pending_df[["Stock", "Qty", "Entry", "StopLoss", "Target"]])
        
        confirm_stock = st.selectbox("Confirm Execution", pending_df['Stock'])
        if st.button("🚀 Confirm Trade Placed"):
            active = pd.read_csv(PATHS["active"])
            row_to_move = pending_df[pending_df['Stock'] == confirm_stock]
            pd.concat([active, row_to_move], ignore_index=True).to_csv(PATHS["active"], index=False)
            pending_df[pending_df['Stock'] != confirm_stock].to_csv(PATHS["pending"], index=False)
            st.rerun()
    else:
        st.info("No pending trades.")

# --- TAB 3: PORTFOLIO & EXIT ---
with tab3:
    active_df = pd.read_csv(PATHS["active"])
    if not active_df.empty:
        st.subheader("Open Positions")
        st.dataframe(active_df, use_container_width=True)
        
        st.divider()
        st.subheader("Exit Management")
        exit_stock = st.selectbox("Select Stock to Exit", active_df['Stock'])
        exit_price = st.number_input("Actual Exit Price", value=0.0)
        
        if st.button("💰 Close Position & Save Log"):
            # Yahan aap P&L calculate karke ek 'history.csv' mein daal sakte hain
            active_df[active_df['Stock'] != exit_stock].to_csv(PATHS["active"], index=False)
            st.success(f"Position closed for {exit_stock}")
            st.rerun()
    else:
        st.info("No active trades.")