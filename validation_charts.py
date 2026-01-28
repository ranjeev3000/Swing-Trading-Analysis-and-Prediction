import webbrowser
import time
import pandas as pd
# Import the function from your screener.py file
from screener import screen_stocks

def open_validation_charts(recommendations_df, platform='tradingview', top_n=10):
    """
    Opens browser tabs for visual review of the screener's output.
    """
    if recommendations_df is None or recommendations_df.empty:
        print("❌ No stocks found by the screener to visualize.")
        return

    # Sort by Volume Ratio to ensure we see the highest conviction trades first
    top_picks = recommendations_df.sort_values(by='Vol_Ratio', ascending=False).head(top_n)

    print(f"\n📺 Preparing to visualize Top {len(top_picks)} picks on {platform.upper()}...")
    print("👀 LOOK FOR: Price stability at EMA 200 and a fresh green candle.")

    for index, row in top_picks.iterrows():
        symbol = row['Stock']
        # Remove suffix for URL construction
        clean_symbol = symbol.replace(".NS", "").replace(".BO", "")
        
        # URL Logic
        if platform.lower() == 'tradingview':
            url = f"https://www.tradingview.com/chart/?symbol=NSE:{clean_symbol}"
        elif platform.lower() == 'zerodha':
            url = f"https://kite.zerodha.com/chart/ext/tvc/NSE:{clean_symbol}"
        elif platform.lower() == 'groww':
            url = f"https://groww.in/search?q={clean_symbol}"
        else:
            url = f"https://www.google.com/finance/quote/{clean_symbol}:NSE"

        print(f"🔗 Opening {clean_symbol} (RSI: {row['RSI']} | Vol Ratio: {row['Vol_Ratio']})...")
        webbrowser.open(url)
        
        # Small delay to let the browser handle the new tab
        time.sleep(1.5)

if __name__ == "__main__":
    print("🚀 Running Screener and Visualizer...")
    
    # 1. Run your screener logic (stored in screener.py)
    # This assumes your CSV data is in a folder named 'data'
    final_list, market_health = screen_stocks('data')
    
    print(f"🌍 Market Health: {market_health:.1f}%")

    # 2. Check if we have results
    if not final_list.empty:
        print(f"\n✅ Found {len(final_list)} potential trades.")
        print(final_list.to_string(index=False))
        
        # 3. Ask for permission to open tabs
        user_choice = input("\nDo you want to open charts for visual validation? (y/n): ")
        if user_choice.lower() == 'y':
            # You can change platform to 'zerodha' or 'groww'
            open_validation_charts(final_list, platform='tradingview', top_n=5)
    else:
        print("\n☹️ No stocks met the criteria today. No charts to open.")