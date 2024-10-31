import yfinance as yf
import pandas as pd
import numpy as np

def replace_nan_with_zero(lst):
    array = np.array(lst, dtype=float)
    array = np.nan_to_num(array, nan=0.0)
    return list(array)

def main():
    # Download SPY price data from 1/2/2020 to 11/11/2022
    data = yf.download('SPY', start='2020-01-02', end='2022-11-12')

    spyOpen = data['Open']

    print(spyOpen)

    spy_data = replace_nan_with_zero(spyOpen)

    pathToFile = '/Users/seanmealey/wsjTest/src/spyOpen.txt'

    with open(pathToFile, 'w') as file:
        for entry in spy_data:
            file.write(f"{entry[0]}\n")

if __name__ == '__main__':
    main()