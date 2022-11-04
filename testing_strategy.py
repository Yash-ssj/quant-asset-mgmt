import os
os.chdir(r'C:\Users\Yashodeep\Documents\Personal\Investment\quant-asset-mgmt')

import pandas as pd
import bktst_utils as butils
import metrics_utils as mutils
from datetime import datetime

#nifty_250 = pd.read_csv(r'C:\\Users\\Yashodeep\\Documents\\Personal\\Investment\\quant-asset-mgmt\\ind_niftysmallcap250list.csv')
nifty_50 = pd.read_csv(r'C:\\Users\\Yashodeep\\Documents\\Personal\\Investment\\quant-asset-mgmt\\ind_nifty50list.csv')

my_strt_dt = datetime.strptime('2019-03-01', '%Y-%m-%d')
my_end_dt = datetime.strptime('2022-11-05', '%Y-%m-%d')

my_universe = mutils.download_ticker_data(ticker_list = nifty_50['Ticker'].unique().tolist(), start_date = '2019-01-01', end_date = '2022-11-05')

price_direction_selections = butils.get_rebal_selections(backtest_strt_dt = my_strt_dt, backtest_end_dt = my_end_dt, rebal_frequency = 2, asset_perf_history = my_universe, invstmt_strategy = 'price_direction', weight_scheme = 'EW')

backtest_strt_dt = my_strt_dt
backtest_end_dt = my_end_dt
rebal_frequency = 2
asset_perf_history = my_universe
invstmt_strategy = 'price_direction'
weight_scheme = 'EW'

#asset_price_series = asset_perf_history[asset_perf_history['Date']<rebal_date]


asset_price_history = my_universe
no_of_days = 10
moving_average_window = 10
shift_days = 0