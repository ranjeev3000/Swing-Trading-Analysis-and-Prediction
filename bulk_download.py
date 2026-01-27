import pandas as pd
import yfinance as yf
import os
import time

def bulk_download_data(input_file, output_folder="data"):
    """
    Downloads 2 years of daily data for symbols in the input CSV.
    Saves each stock's data as a separate CSV file.
    """
    # 1. Create the data directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 Created directory: {output_folder}")

    # 2. Read the symbols from your Nifty 200 list
    try:
        df_symbols = pd.read_csv(input_file)
        # Ensure we use the correct column name from your file
        symbols = df_symbols['Symbol'].tolist()
    except Exception as e:
        print(f"❌ Error reading {input_file}: {e}")
        return

    print(f"🚀 Starting download of {len(symbols)} stocks...")
    
    success_count = 0
    fail_count = 0

    # 3. Download loop
    for i, ticker in enumerate(symbols):
        try:
            print(f"[{i+1}/{len(symbols)}] Downloading {ticker}...", end="\r")
            
            # Fetch 2 years of daily data
            # auto_adjust=True handles dividends/splits (essential for Moving Averages)
            data = yf.download(ticker, period="2y", interval="1d", progress=False, auto_adjust=True)
            
            if not data.empty:
                # Save as TickerName.csv (e.g., RELIANCE.NS.csv)
                file_path = os.path.join(output_folder, f"{ticker}.csv")
                data.to_csv(file_path)
                success_count += 1
            else:
                print(f"\n⚠️ No data found for {ticker}")
                fail_count += 1
                
            # Anti-throttling: Small sleep to be polite to Yahoo Finance servers
            time.sleep(0.2)

        except Exception as e:
            print(f"\n❌ Failed to download {ticker}: {e}")
            fail_count += 1

    print(f"\n\n✅ Download Complete!")
    print(f"📊 Successfully saved: {success_count} files in '{output_folder}/'")
    print(f"⚠️ Failed/Missing: {fail_count}")

if __name__ == "__main__":
    # Point this to the file you just shared with me
    input_csv = "nifty_200_indexed.csv"
    bulk_download_data(input_csv)