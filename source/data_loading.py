import os
from equity_names import Equity

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

data_path = r'../data/ohlc-us/'
available_tickers = [ticker for ticker in Equity.get_all_keys()
                     if f'{ticker.lower()}.us.txt' in os.listdir(data_path) ]


def get_log_close_values(ticker_name, start_date='2015-10-20', end_date='2017-11-20', window_length=11, polyorder=3):
    # Load the data into a DataFrame
    df = pd.read_csv(os.path.join(data_path, f'{ticker_name.lower()}.us.txt'))

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert input dates to datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter rows between start_date and end_date
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered_df = df.loc[mask]

    # Calculate the natural log of 'Close' values as a numpy array
    log_close_values = np.log(filtered_df['Close'].values)

    # Apply Savitzky-Golay filtering to the log values
    smoothed_values = savgol_filter(log_close_values, window_length, polyorder)

    return smoothed_values


def plot_smoothed_vs_unsmoothed(ticker_name, start_date='2015-10-20', end_date='2017-11-20', window_length=11, polyorder=3):
    # Load the data into a DataFrame
    df = pd.read_csv(os.path.join(data_path, f'{ticker_name.lower()}.us.txt'))

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert input dates to datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter rows between start_date and end_date
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered_df = df.loc[mask]

    # Calculate the natural log of 'Close' values as a numpy array
    log_close_values = np.log(filtered_df['Close'].values)

    # Apply Savitzky-Golay filtering to the log values
    smoothed_values = savgol_filter(log_close_values, window_length, polyorder)

    # Plot the smoothed vs. unsmoothed data
    plt.figure(figsize=(12, 6))
    plt.plot(filtered_df['Date'], log_close_values, label='Unsmoothed', color='blue')
    plt.plot(filtered_df['Date'], smoothed_values, label='Smoothed', color='red')
    plt.title(f'{ticker_name} Log Close Values')
    plt.xlabel('Date')
    plt.ylabel('Log Close Value')
    plt.legend()
    plt.grid(True)
    plt.show()