import pandas as pd
import numpy as np
from datetime import datetime
import metrics_utils as qutils

def generate_weights(no_of_assets, weighting_scheme = 'EW'):
  if weighting_scheme == 'EW':
    cons_weights = [1.000000/no_of_assets] * no_of_assets
  
  return cons_weights

def price_direction_strategy(asset_price_series, price_dirs = [0, 5, 10, 15, 20]):
  ticker_selection = []
  for x in asset_price_series['Ticker'].unique().tolist():
    z = 0
    for y in price_dirs:
      z = z + qutils.get_price_direction(asset_price_history = asset_price_series[asset_price_series['Ticker']==x], no_of_days = 10, shift_days = y)
    if z >= 5:
      ticker_selection.append(x)
  return ticker_selection

def calc_backtest_returns(asset_price_history, backtest_portfolio_alloc):
  asset_price_history = qutils.get_price_returns(asset_price_history = asset_price_history)
  
  calc_dates = sorted(asset_price_history['Date'].unique().tolist())
  initial_inv = 100000.000000
  rebal_dates = sorted(backtest_portfolio_alloc['Date'].unique().tolist()))
  asset_price_history['isRebalDate'] = np.where(asset_price_history['Date'] in rebal_dates, 1, 0)
  asset_price_history['Rebal'] = rebal_dates[0]
  
  
  my_strategy_series = pd.DataFrame(columns = ['Date','portf_val'])
  my_strategy_series.loc[0] = [rebal_dates[0], initial_inv]
  
    
  

def get_rebal_selections(backtest_strt_dt, backtest_end_dt, rebal_frequency, asset_perf_history, invstmt_strategy = 'price_direction', weight_scheme = 'EW'):
  bktst_alloc = pd.DataFrame(columns = ['Date','Ticker','Weight'])
  #no_of_rebals = (datetime.strptime(backtest_end_dt, '%Y-%m-%d') - datetime.strptime(backtest_strt_dt, '%Y-%m-%d'))
  #rebal_dts = [datetime.strptime(backtest_strt_dt, '%Y-%m-%d') + relativedelta(months = rebal_frequency) * i for i in [0,]]
  rebal_date = backtest_strt_dt
  while rebal_date <= backtest_end_dt:
    rebal_selections = price_direction_strategy(asset_perf_history)
    col1 = [rebal_date]*len(rebal_selections)
    bktst_alloc_dict = {"Date":[rebal_date]*len(rebal_selections), "Ticker":rebal_selections, "Weight": generate_weights(no_of_assets = len(rebal_selections), weighting_scheme = weight_scheme)}
    bktst_alloc_df = pd.DataFrame(bktst_alloc_dict.items(), columns = bktst_alloc_dict.keys().tolist())
    bktst_alloc = pd.concat([bktst_alloc, bktst_alloc_df],ignore_index=True)
    rebal_date = [datetime.strptime(rebal_date, '%Y-%m-%d') + relativedelta(months = rebal_frequency)
  return bktst_alloc
    
    
  
