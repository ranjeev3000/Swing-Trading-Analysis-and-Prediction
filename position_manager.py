import pandas as pd
import datetime

def position_manager():
    try:
        df = pd.read_csv('screener/screened_output.csv')
    except FileNotFoundError:
        print("❌ No screened stocks found. Run screener.py first.")
        return

    print("\n--- 💰 POSITION & MARGIN MANAGER ---")
    capital = float(input("Enter your available cash (e.g., 2000): "))
    print("Choose Margin: [1] No Margin (1x) | [2] Intraday (2x) | [4] MTF (4x)")
    leverage = int(input("Selection: "))
    
    buying_power = capital * leverage
    risk_per_trade = capital * 0.05 # Risking 5% of cash per trade
    
    pending_list = []
    
    for _, row in df.iterrows():
        price = row['Price']
        sl = row['Stop_Loss']
        
        # Position Sizing
        risk_per_share = price - sl
        qty = int(min(risk_per_trade / risk_per_share, buying_power / price))
        
        if qty > 0:
            pending_list.append({
                "Date": datetime.date.today(),
                "Stock": row['Stock'],
                "Entry": price,
                "Qty": qty,
                "SL": sl,
                "Target": row['Target'],
                "Strategy": "RSI Pullback + EMA Support",
                "Margin_Used": leverage
            })

    pending_df = pd.DataFrame(pending_list)
    pending_df.to_csv('screener/pending_trades.csv', index=False)
    print("\n✅ Pending trades saved to pending_trades.csv")
    print(pending_df.to_string(index=False))

if __name__ == "__main__":
    position_manager()