import requests
import pandas as pd
import io

def get_nse_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers, timeout=10)
    response = session.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        return pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    return None

def get_full_index_mapping():
    """
    Downloads major sectoral/thematic lists to map which stock belongs where.
    """
    indices_to_track = {
        "NIFTY 50": "https://archives.nseindia.com/content/indices/ind_nifty50list.csv",
        "NIFTY BANK": "https://archives.nseindia.com/content/indices/ind_niftybanklist.csv",
        "NIFTY IT": "https://archives.nseindia.com/content/indices/ind_niftyitlist.csv",
        "NIFTY PHARMA": "https://archives.nseindia.com/content/indices/ind_niftypharmalist.csv",
        "NIFTY FMCG": "https://archives.nseindia.com/content/indices/ind_niftyfmcglist.csv"
    }
    
    mapping = {}
    for name, url in indices_to_track.items():
        print(f"Fetching constituents for {name}...")
        df = get_nse_data(url)
        if df is not None:
            for symbol in df['Symbol'].unique():
                symbol = symbol.strip()
                if symbol not in mapping:
                    mapping[symbol] = []
                mapping[symbol].append(name)
    return mapping

def download_and_map_nifty_200():
    # 1. Download the master Nifty 200 list
    print("Downloading Master Nifty 200 List...")
    master_url = "https://archives.nseindia.com/content/indices/ind_nifty200list.csv"
    df_200 = get_nse_data(master_url)
    
    if df_200 is None:
        return
    
    # 2. Get the mappings for Sectoral/Major indices
    index_map = get_full_index_mapping()
    
    # 3. Clean and Format
    df_200['Symbol'] = df_200['Symbol'].str.strip()
    
    # 4. Map the indices (Join multiple indices with a comma)
    df_200['Detailed_Indices'] = df_200['Symbol'].map(lambda x: ", ".join(index_map.get(x, ["NIFTY 200 Only"])))
    
    # 5. Add .NS for your analysis
    df_200['Symbol'] = df_200['Symbol'] + ".NS"
    
    # Save results
    df_200.to_csv("nifty_200_indexed.csv", index=False)
    print("\n✅ Process Complete!")
    print(df_200[['Symbol', 'Detailed_Indices']].head(10))

if __name__ == "__main__":
    download_and_map_nifty_200()