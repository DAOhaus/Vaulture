import os
import requests
import numpy as np
import pandas as pd

CMC_API_KEY = 'f0a82a73-dd69-4322-8510-b86763fab4d4'
CMC_BASE_URL = 'https://pro-api.coinmarketcap.com/v1/'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CMC_API_KEY,
}

# Define the paths
base_path = r"2024 August Superhack"
sentiment_path = os.path.join(base_path, "Augmento AI", "Aggregated Sentiments")

def get_crypto_data(symbols):
    url = f'{CMC_BASE_URL}cryptocurrency/quotes/latest'
    parameters = {
        'symbol': ','.join(symbols),
        'convert': 'USD'
    }
    response = requests.get(url, headers=headers, params=parameters).json()
    return response['data']

def get_historical_data(symbol, time_start, time_end, interval='daily'):
    url = f'{CMC_BASE_URL}cryptocurrency/ohlcv/historical'
    parameters = {
        'symbol': symbol,
        'convert': 'USD',
        'time_start': time_start,
        'time_end': time_end,
        'interval': interval
    }
    response = requests.get(url, headers=headers, params=parameters).json()
    return response['data']['quotes']

def calculate_volatility(prices):
    """Calculate price volatility as the standard deviation of price changes."""
    returns = np.diff(prices) / prices[:-1]
    volatility = np.std(returns)
    return volatility

def normalize(value, min_val, max_val):
    """Normalize the value to a range of 0 to 100."""
    return 100 * (value - min_val) / (max_val - min_val)

def calculate_fear_greed_index(volatility, momentum_volume, dominance, sentiment):
    """Calculate the Fear and Greed Index."""
    index = (
        0.25 * volatility +
        0.25 * momentum_volume +
        0.10 * dominance +
        0.15 * sentiment  # Assuming sentiment contributes 15%
    )
    return round(index, 2)

def get_sentiment_index(symbol):
    """Fetch the sentiment index from the relevant Excel file."""
    file_name = f"{symbol}_agg.xlsx"
    file_path = os.path.join(sentiment_path, file_name)
    
    if not os.path.exists(file_path):
        print(f"Sentiment file for {symbol} not found.")
        return None
    
    # Load the sentiment data
    df = pd.read_excel(file_path)
    
    # Example: Assuming sentiment index is calculated as the mean of a specific column
    sentiment_index = df['sentiment_score'].mean()  # Replace with actual column name and calculation
    return sentiment_index

def main(symbols):
    # Historical data: last 90 days
    time_start = '2022-01-01'  # Example start date
    time_end = '2022-03-31'  # Example end date

    for symbol in symbols:
        # Fetch historical data for the symbol
        historical_data = get_historical_data(symbol, time_start, time_end)
        prices = [quote['close'] for quote in historical_data]
        
        # Calculate volatility based on the last 30 days
        volatility_30d = calculate_volatility(prices[-30:])
        
        # Calculate average volume over the last 30 and 90 days
        volumes = [quote['volume'] for quote in historical_data]
        avg_volume_30d = np.mean(volumes[-30:])
        avg_volume_90d = np.mean(volumes)

        # Fetch the latest market data for the symbol
        latest_data = get_crypto_data([symbol])
        current_volume = latest_data[symbol]['quote']['USD']['volume_24h']

        # Calculate market momentum/volume index
        volume_diff_30d = abs(current_volume - avg_volume_30d) / avg_volume_30d
        volume_diff_90d = abs(current_volume - avg_volume_90d) / avg_volume_90d
        momentum_volume_index = normalize((volume_diff_30d + volume_diff_90d) / 2, 0, 1)

        # Fetch global metrics to get dominance (assuming BTC dominance is used)
        dominance_url = f'{CMC_BASE_URL}global-metrics/quotes/latest'
        global_metrics = requests.get(dominance_url, headers=headers).json()
        current_dominance = global_metrics['data']['btc_dominance']

        # Normalize dominance
        dominance_index = normalize(current_dominance, 0, 100)

        # Get sentiment index from the relevant Excel file
        sentiment_index = get_sentiment_index(symbol)
        if sentiment_index is None:
            continue  # Skip if sentiment data is missing

        # Calculate the Fear and Greed Index
        fear_greed_index = calculate_fear_greed_index(volatility_30d, momentum_volume_index, dominance_index, sentiment_index)

        print(f"Symbol: {symbol}")
        print(f"Volatility Index: {volatility_30d}")
        print(f"Momentum/Volume Index: {momentum_volume_index}")
        print(f"Dominance Index: {dominance_index}")
        print(f"Sentiment Index: {sentiment_index}")
        print(f"Fear and Greed Index: {fear_greed_index}")
        print("="*30)

if __name__ == "__main__":
    symbols = ['BTC', 'ETH', 'DOGE', 'USDT', 'AAVE', 'LINK', 'ALGO', 'AVAX']  # Example symbols list, add more as needed
    main(symbols)
