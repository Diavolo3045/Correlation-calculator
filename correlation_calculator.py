import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import os

def calculate_correlation(btc_data, asset_data):
    merged = pd.merge(btc_data, asset_data, left_index=True, right_index=True, suffixes=('_btc', '_asset'))
    correlation = merged['close_btc'].corr(merged['close_asset'])
    return correlation

def get_data_for_timeframe(symbol, timeframe):
    filename = os.path.join('data', f"{symbol.replace('/', '_').replace(':', '_')}_{timeframe}.csv")
    if not Path(filename).is_file():
        print(f"Warning: File {filename} not found. Skipping.")
        return None

    df = pd.read_csv(filename, index_col='timestamp', parse_dates=True)
    df = df.sort_index()  # Ensure data is sorted by timestamp

    now = datetime.utcnow()
    if timeframe == '1m':
        start_time = now - timedelta(hours=1)
    elif timeframe == '5m':
        start_time = now - timedelta(hours=6)
    elif timeframe == '30m':
        start_time = now - timedelta(days=1)
    elif timeframe == '1h':
        start_time = now - timedelta(days=1)
    elif timeframe == '1d':
        start_time = now - timedelta(days=30)
    else:
        raise ValueError(f"Unsupported timeframe: {timeframe}")

    return df[df.index >= start_time]

def main():
    base_symbol = 'BTC/USDT:USDT'  # BTC-PERP
    symbols = ['ETH/USDT:USDT', 'POPCAT/USDT:USDT','WIF/USDT:USDT']  # Add more symbols as needed
    timeframes = ['1m', '5m', '30m', '1h', '1d']

    results = []

    for timeframe in timeframes:
        btc_data = get_data_for_timeframe(base_symbol, timeframe)
        if btc_data is None:
            continue

        for symbol in symbols:
            asset_data = get_data_for_timeframe(symbol, timeframe)
            if asset_data is None:
                continue

            correlation = calculate_correlation(btc_data, asset_data)
            results.append({
                'symbol': symbol,
                'timeframe': timeframe,
                'correlation': correlation,
                'relationship': 'Positive' if correlation > 0 else 'Negative',
                'data_points': len(btc_data)
            })

    return results

if __name__ == "__main__":
    correlation_results = main()
    for result in correlation_results:
        print(f"{result['symbol']} - {result['timeframe']}: Correlation: {result['correlation']:.4f} "
              f"({result['relationship']}) - Data points: {result['data_points']}")
