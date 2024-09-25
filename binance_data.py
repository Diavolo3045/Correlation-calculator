import ccxt
import pandas as pd
from datetime import datetime, timedelta
import os

def ensure_data_folder_exists():
    if not os.path.exists('data'):
        os.makedirs('data')

def download_futures_ohlcv(symbol, timeframe, start_date, end_date):
    exchange = ccxt.binance({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future'
        }
    })

    ohlcv = []

    while start_date < end_date:
        chunk = exchange.fetch_ohlcv(symbol, timeframe, exchange.parse8601(start_date.isoformat()), limit=1000)
        ohlcv.extend(chunk)
        if len(chunk) == 0:
            break
        start_date = datetime.fromtimestamp(chunk[-1][0] / 1000) + timedelta(minutes=1)

    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def main():
    ensure_data_folder_exists()
    base_symbol = 'BTC/USDT:USDT'  # BTC-PERP
    symbols = ['ETH/USDT:USDT', 'POPCAT/USDT:USDT']  # Add more symbols as needed
    timeframes = ['1m', '5m', '30m', '1h', '1d']
    end_date = datetime.utcnow()

    all_symbols = [base_symbol] + symbols

    for symbol in all_symbols:
        for timeframe in timeframes:
            if timeframe == '1m':
                start_date = end_date - timedelta(hours=2)  # Extra hour for safety
            elif timeframe == '5m':
                start_date = end_date - timedelta(hours=7)  # Extra hour for safety
            elif timeframe == '30m':
                start_date = end_date - timedelta(days=2)   # Extra day for safety
            elif timeframe == '1h':
                start_date = end_date - timedelta(days=2)   # Extra day for safety
            elif timeframe == '1d':
                start_date = end_date - timedelta(days=31)  # Extra day for safety

            df = download_futures_ohlcv(symbol, timeframe, start_date, end_date)
            filename = os.path.join('data', f"{symbol.replace('/', '_').replace(':', '_')}_{timeframe}.csv")
            df.to_csv(filename)
            print(f"Saved {filename} with {len(df)} data points")

if __name__ == "__main__":
    main()
