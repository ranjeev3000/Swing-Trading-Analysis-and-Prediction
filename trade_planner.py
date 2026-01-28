import pandas as pd
from screener import screen_stocks  # Importing your screener logic

def generate_trade_report(screened_stocks, total_capital=2000, risk_per_trade=100):
    """
    Refined Trade Planner:
    - screened_stocks: Data from screener.py
    - total_capital: Your available cash (₹2000)
    - risk_per_trade: Maximum loss allowed per trade (₹100)
    """
    if screened_stocks.empty:
        return pd.DataFrame()
    
    MTF_MARGIN = 4  # 4x Buying power
    BUYING_POWER = total_capital * MTF_MARGIN
    
    planned_trades = []

    for _, row in screened_stocks.iterrows():
        symbol = row['Stock']
        price = row['Price']
        sl = row['Stop_Loss']
        target = row['Target']
        
        # 1. Calculation of Risk & Reward per share
        risk_per_share = price - sl
        reward_per_share = target - price
        
        if risk_per_share <= 0:
            continue

        # 2. Position Sizing (The most important part)
        # Rule A: Based on Risk (Max loss ₹100)
        qty_risk = int(risk_per_trade / risk_per_share)
        
        # Rule B: Based on Capital (Max ₹8000 buying power)
        qty_cap = int(BUYING_POWER / price)
        
        # Take the minimum of the two
        final_qty = min(qty_risk, qty_cap)
        
        if final_qty <= 0:
            continue

        # 3. Financial Breakdown
        trade_value = final_qty * price
        cash_used = trade_value / MTF_MARGIN
        
        # 4. Realistic Net Profit (Gross Profit - Brokerage - STT/Taxes)
        gross_profit = reward_per_share * final_qty
        # Estimate: ₹40 flat + 0.05% of total trade value for taxes
        est_charges = 40 + (trade_value * 0.0005)
        net_profit = gross_profit - est_charges
        
        rr_ratio = round(reward_per_share / risk_per_share, 2)

        # 5. BEST RESULT FILTER: Only keep trades with R:R > 1.5
        if rr_ratio >= 1.5:
            planned_trades.append({
                "Stock": symbol,
                "Entry": price,
                "Qty": final_qty,
                "StopLoss": sl,
                "Target": target,
                "R:R": rr_ratio,
                "Capital_Needed": round(cash_used, 2),
                "Max_Risk": round(risk_per_share * final_qty, 2),
                "Net_Profit_Est": round(net_profit, 2),
                "Hold_Period": row['Estimated_Hold']
            })

    return pd.DataFrame(planned_trades)

# --- EXECUTION ENGINE ---
if __name__ == "__main__":
    # CONFIGURATION
    YOUR_CASH = 2000 
    MAX_LOSS_PER_TRADE = 100
    DATA_FOLDER = 'data' # Path to your CSV files

    print(f"🚀 [1/3] Running Screener on '{DATA_FOLDER}'...")
    screened_data, health = screen_stocks(DATA_FOLDER)
    
    print(f"🌍 Market Health: {health:.1f}%")

    if not screened_data.empty:
        print(f"💰 [2/3] Found {len(screened_data)} candidates. Planning trades for ₹{YOUR_CASH}...")
        report = generate_trade_report(screened_data, total_capital=YOUR_CASH, risk_per_trade=MAX_LOSS_PER_TRADE)
        
        if not report.empty:
            print("\n--- 📝 OPTIMIZED TRADE PLAN ---")
            # Sort by Net Profit to see the best opportunities first
            print(report.sort_values(by='Net_Profit_Est', ascending=False).to_string(index=False))
            
            print(f"\n✅ Total Opportunities Found: {len(report)}")
            print("💡 Action: Pick the top 1-2 stocks based on Net_Profit_Est.")
        else:
            print("\n☹️ No trades offer a good Risk-to-Reward ratio for your budget.")
    else:
        print("\n☹️ No stocks found by the screener. No planning possible.")