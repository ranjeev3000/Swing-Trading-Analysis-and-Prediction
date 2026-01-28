import pandas as pd
import pandas_ta as ta
import os
"""
💡 Strategy Cheat-Sheet for this Script:
Market Health < 40%: The market is weak. Even if you find a stock, be careful.

Market Health > 60%: The market is strong. These "dip-buys" have a very high chance of success.

The Stop Loss: I used 1.5 * ATR. This is tight enough to protect your capital but wide enough to let the stock breathe.

The Target: I used 3.0 * ATR. This ensures you make twice as much as you risk (1:2 ratio).

You have now built a professional-grade end-to-end pipeline: Download -> Format -> Clean -> Screen -> Risk Manage. Happy trading!



🚩 Pro-Tip: How to read "Market Health"
If Health < 40%: The overall Nifty 200 is weak. Even if the script finds a stock, be very cautious. Reduce your position size.

If Health > 60%: The wind is at your back. You can be more aggressive with your entries.
"""
def screen_stocks(folder_path):
    recommendations = []
    bullish_count = 0
    total_files = 0
    
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder '{folder_path}' not found.")
        return pd.DataFrame(), 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            total_files += 1
            file_path = os.path.join(folder_path, filename)
            
            try:
                df = pd.read_csv(file_path)
                # Cleanup headers
                if "Ticker" in df.columns.tolist() or "Price" in df.columns.tolist():
                    df = pd.read_csv(file_path, header=[0, 1], index_col=0)
                    df.columns = df.columns.get_level_values(0)
                
                if 'Date' in df.columns: df.set_index('Date', inplace=True)
                close_col = next((c for c in df.columns if str(c).lower() in ['close', 'adj close']), None)
                vol_col = next((c for c in df.columns if str(c).lower() == 'volume'), None)
                
                df[close_col] = pd.to_numeric(df[close_col], errors='coerce')
                df.dropna(subset=[close_col], inplace=True)
                if len(df) < 200: continue
                
                # 1. Indicators
                df['EMA_50'] = ta.ema(df[close_col], length=50)
                df['EMA_200'] = ta.ema(df[close_col], length=200)
                df['RSI'] = ta.rsi(df[close_col], length=14)
                df['ATR'] = ta.atr(df['High'], df['Low'], df[close_col], length=14)
                
                # 2. Volume
                df['Vol_Avg_20'] = df[vol_col].rolling(window=20).mean()
                last_3d_vol_avg = df[vol_col].tail(3).mean()
                
                last_row = df.iloc[-1]
                price = last_row[close_col]
                
                # Market Breadth check
                if price > last_row['EMA_200']: bullish_count += 1

                # --- FILTERS ---
                is_bullish = (price > last_row['EMA_200']) and (price > last_row['EMA_50'])
                is_rsi_zone = (30 <= last_row['RSI'] <= 50) 
                is_vol_surge = (last_3d_vol_avg > last_row['Vol_Avg_20'])

                if is_bullish and is_rsi_zone and is_vol_surge:
                    atr_val = last_row['ATR']
                    stop_loss = price - (1.5 * atr_val)
                    target = price + (3.0 * atr_val)
                    
                    # Logic for Estimated Hold:
                    # If RSI is very low (<35), it's a deep reversal, might take longer.
                    # If Volume surge is huge (>2.0), move might happen fast.
                    vol_ratio = last_3d_vol_avg / last_row['Vol_Avg_20']
                    if vol_ratio > 2.0:
                        hold_period = "3-7 Days (Fast Move)"
                    elif last_row['RSI'] < 35:
                        hold_period = "10-15 Days (Recovery)"
                    else:
                        hold_period = "5-10 Days (Standard Swing)"

                    recommendations.append({
                        "Stock": filename.replace(".csv", "").replace(".NS", ""),
                        "Price": round(price, 2),
                        "RSI": round(last_row['RSI'], 2),
                        "Vol_Ratio": round(vol_ratio, 2),
                        "Stop_Loss": round(stop_loss, 2),
                        "Target": round(target, 2),
                        "Estimated_Hold": hold_period
                    })
                    
            except Exception: continue
                
    breadth = (bullish_count / total_files) * 100 if total_files > 0 else 0
    return pd.DataFrame(recommendations), breadth

# Run the Scanner
print("🔍 Scanning for high-probability setups...")
final_list, market_breadth = screen_stocks('data')

print(f"\n🌍 MARKET HEALTH: {market_breadth:.1f}% of Nifty 200 is in an Uptrend.")

if not final_list.empty:
    print("\n--- 🚀 SWING TRADING OPPORTUNITIES ---")
    print(final_list.sort_values(by='Vol_Ratio', ascending=False).to_string(index=False))
    # Save for position_manager.py to pick up
    final_list.to_csv('screened_output.csv', index=False)
    print("✅ Screened results exported to screened_output.csv")
else:
    print("\n☹️ No stocks met criteria. Cash is a position!")