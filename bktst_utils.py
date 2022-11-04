import pandas as pd
import numpy as np
from datetime import datetime
import metrics_utils as qutils
from dateutil.relativedelta import relativedelta

def generate_weights(no_of_assets, weighting_scheme = 'EW'):
  if weighting_scheme == 'EW':
    cons_weights = [1.000000/no_of_assets] * no_of_assets
  
  return cons_weights

def price_direction_strategy(asset_price_series, price_dirs = [0, 5, 10, 15, 20]):
  ticker_selection = []
  for x in asset_price_series['Ticker'].unique().tolist():
    z = 0
    for y in price_dirs:
      z = z + qutils.get_price_direction(asset_price_history = asset_price_series[asset_price_series['Ticker']==x].reset_index(), no_of_days = 10, shift_days = y)
    if z >= 5:
      ticker_selection.append(x)
  return ticker_selection

def benchmark_strategy(asset_price_series):
  return asset_price_series['Ticker'].unique().tolist()

def calc_backtest_returns(asset_price_history, backtest_portfolio_alloc):
  asset_price_history = qutils.get_price_returns(asset_price_history = asset_price_history)
  
  calc_dates = sorted(asset_price_history['Date'].unique().tolist())
  port_val = 100000.000000
  rebal_dates = sorted(backtest_portfolio_alloc['Date'].unique().tolist())
  asset_price_history['isRebalDate'] = np.where(asset_price_history['Date'] in rebal_dates, 1, 0)
  #asset_price_history['Rebal'] = rebal_dates[0]
  my_strategy_series = pd.DataFrame(columns = ['Date','portf_val'])
  asset_price_history = pd.merge(asset_price_history, backtest_portfolio_alloc, on = ['Date','Ticker'], how = 'left')
  asset_price_history['AssetValue'] = 0.000000
  portfolio_cons_bktst = pd.DataFrame(columns = asset_price_history.columns.tolist())
  for i in calc_dates:
    asset_prices = asset_price_history[asset_price_history['Date']==i]
    if asset_prices.loc[0]['isRebalDate'] == 1:
      #portfolio_alloc = backtest_portfolio_alloc[backtest_portfolio_alloc['Date']==i]
      asset_prices['AssetValue'] = port_val * asset_prices['Weight'] * asset_prices['1_day_return']
      portfolio_cons_bktst = pd.concat(portfolio_cons_bktst, asset_prices)
      my_strategy_series = pd.concat(my_strategy_series, pd.DataFrame({'Date': i, 'portf_val': asset_prices['AssetValue'].sum()}.items()))
      port_val = asset_prices['AssetValue'].sum()
    else:
      prev_date = calc_dates[calc_dates.index(i)-1]
      prev_asset_prices = portfolio_cons_bktst[portfolio_cons_bktst['Date'] == prev_date]
      prev_asset_prices.rename(columns={'AssetValue' : 'AssetValue_PrevDay'},inplace=True)
      asset_prices = asset_prices.merge(prev_asset_prices[['Ticker','AssetValue_PrevDay']], on = 'Ticker', how = 'on')
      asset_prices['AssetValue'] = asset_prices['AssetValue_PrevDay'] * asset_prices['1_day_return']
      portfolio_cons_bktst = pd.concat(portfolio_cons_bktst, asset_prices[asset_price_history.columns.tolist()])
      my_strategy_series = pd.concat(my_strategy_series, pd.DataFrame({'Date': i, 'portf_val': asset_prices['AssetValue'].sum()}.items()))
      port_val = asset_prices['AssetValue'].sum()
  
  return my_strategy_series

def get_rebal_selections(backtest_strt_dt, backtest_end_dt, rebal_frequency, asset_perf_history, invstmt_strategy = 'price_direction', weight_scheme = 'EW'):
  bktst_alloc = pd.DataFrame(columns = ['Date','Ticker','Weight'])
  #no_of_rebals = (datetime.strptime(backtest_end_dt, '%Y-%m-%d') - datetime.strptime(backtest_strt_dt, '%Y-%m-%d'))
  #rebal_dts = [datetime.strptime(backtest_strt_dt, '%Y-%m-%d') + relativedelta(months = rebal_frequency) * i for i in [0,]]
  rebal_date = backtest_strt_dt
  while rebal_date <= backtest_end_dt:
    rebal_selections = eval(invstmt_strategy+'_strategy'+"(asset_perf_history[asset_perf_history['Date']<rebal_date])")
    #col1 = [rebal_date]*len(rebal_selections)
    if not len(rebal_selections) == 0:
        bktst_alloc_dict = {"Date":[rebal_date]*len(rebal_selections), "Ticker":rebal_selections, "Weight": generate_weights(no_of_assets = len(rebal_selections), weighting_scheme = weight_scheme)}
        bktst_alloc_df = pd.DataFrame.from_dict(bktst_alloc_dict)#(bktst_alloc_dict.values(), columns = list(bktst_alloc_dict.keys()))
        bktst_alloc = pd.concat([bktst_alloc, bktst_alloc_df],ignore_index=True)
    #rebal_date = datetime.strptime(rebal_date, '%Y-%m-%d') + relativedelta(months = rebal_frequency)
    rebal_date = rebal_date + relativedelta(months = rebal_frequency)
  
  return bktst_alloc


