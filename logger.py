import pandas as pd
import os

def log_execution():
    if not os.path.exists('screener/pending_trades.csv'):
        print("❌ No pending trades to log.")
        return

    pending = pd.read_csv('screener/pending_trades.csv')
    active_file = 'screener/active_trades.csv'
    
    # Load existing active trades or create new
    if os.path.exists(active_file):
        active_df = pd.read_csv(active_file)
    else:
        active_df = pd.DataFrame()

    new_active_trades = []
    remaining_pending = []

    print("\n--- 📒 TRADE EXECUTION LOG ---")
    for _, row in pending.iterrows():
        print(f"\nSTOCK: {row['Stock']} | Entry: {row['Entry']} | Qty: {row['Qty']}")
        status = input(f"Did you execute this on your broker? (y/n): ").lower()
        
        if status == 'y':
            new_active_trades.append(row)
            print(f"✔️ Moved {row['Stock']} to Active Journal.")
        else:
            remaining_pending.append(row)
            print(f"❌ {row['Stock']} remains in Pending.")

    # Update CSVs
    if new_active_trades:
        updated_active = pd.concat([active_df, pd.DataFrame(new_active_trades)], ignore_index=True)
        updated_active.to_csv(active_file, index=False)
    
    pd.DataFrame(remaining_pending).to_csv('pending_trades.csv', index=False)
    print("\n✅ Journals Updated.")

if __name__ == "__main__":
    log_execution()