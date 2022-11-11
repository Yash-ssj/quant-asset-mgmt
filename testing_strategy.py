import os
os.chdir(r'C:\Users\Yashodeep\Documents\Personal\Investment\quant-asset-mgmt')

import pandas as pd
import bktst_utils as butils
import metrics_utils as mutils
from datetime import datetime

nifty_250 = pd.read_csv(r'C:\\Users\\Yashodeep\\Documents\\Personal\\Investment\\quant-asset-mgmt\\ind_niftysmallcap250list.csv')
#nifty_50 = pd.read_csv(r'C:\\Users\\Yashodeep\\Documents\\Personal\\Investment\\quant-asset-mgmt\\ind_nifty50list.csv')

my_strt_dt = datetime.strptime('2019-03-01', '%Y-%m-%d')
my_end_dt = datetime.strptime('2022-11-05', '%Y-%m-%d')

my_universe = mutils.download_ticker_data(ticker_list = nifty_250['Ticker'].unique().tolist(), start_date = '2019-01-01', end_date = '2022-11-05')

price_direction_selections = butils.get_rebal_selections(backtest_strt_dt = my_strt_dt, backtest_end_dt = my_end_dt, rebal_frequency = 2, asset_perf_history = my_universe, invstmt_strategy = 'price_direction', weight_scheme = 'EW')

#price_direction_selections.to_excel('price_direction_selections_nifty250.xlsx',index=False)

backtest_perf = butils.calc_backtest_returns(asset_price_history = my_universe, backtest_portfolio_alloc = price_direction_selections)

##Performance Comparison
my_strgy_perf = backtest_perf.rename(columns = {'portf_val':'Close'})

my_strgy_perf['Ticker'] = 'price_direction_strategy'
my_strgy_perf = my_strgy_perf[['Ticker', 'Date', 'Close']]

#mutils.plot_price_history(asset_price_history = my_strgy_perf, start_date = my_strt_dt, end_date=my_end_dt)

nifty250_hist = mutils.download_ticker_data(ticker_list = ['0P0001IAUC.BO'], start_date = '2019-01-01', end_date = '2022-11-05')
#nifty250_hist.columns
nifty250_hist = nifty250_hist[['Ticker','Date','Close']]

price_time_series = mutils.concat_price_series([my_strgy_perf, nifty250_hist])
mutils.plot_perf_comparison(price_time_series)
#mutils.plot_price_history(asset_price_history = nifty250_hist, start_date = my_strt_dt, end_date=my_end_dt)

indexes_hist = mutils.download_ticker_data(ticker_list = ['^NSEI','^NDX'], start_date = '2000-01-01', end_date = '2022-11-12')
price_time_series = mutils.concat_price_series([indexes_hist[indexes_hist['Ticker']==x][['Ticker','Date','Close']] for x in indexes_hist['Ticker'].unique().tolist()])
price_time_series = mutils.concat_price_series(indexes_hist[['Ticker','Date','Close']],start_date=datetime.strptime('2020-03-31', '%Y-%m-%d'))
mutils.plot_perf_comparison(price_time_series)

type(indexes_hist['Ticker'].unique().tolist())

price_time_series.groupby('Ticker')['Date'].min().reset_index().merge(price_time_series, on=['Ticker','Date'], how='inner')

##Testing- QA

#backtest_strt_dt = my_strt_dt
#backtest_end_dt = my_end_dt
#rebal_frequency = 2
#asset_perf_history = my_universe
#invstmt_strategy = 'price_direction'
#weight_scheme = 'EW'

#asset_price_series = asset_perf_history[asset_perf_history['Date']<rebal_date]

#asset_price_history = my_universe
#no_of_days = 10
#moving_average_window = 10
#shift_days = 0
