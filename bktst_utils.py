from datetime import datetime
import metrics_utils as qutils

def generate_weights(no_of_assets, weighting_scheme = 'EW'):
  if weighting_scheme == 'EW':
    cons_weights = [1.000000/no_of_assets] * no_of_assets
  
  return cons_weights

def price_direction_strategy(asset_price_series, price_dirs = [3, 5, 10, 20]):
  ticker_selection = []
  for x in asset_price_series['Ticker'].unique().tolist():
    z = 0
    for y in sorted(price_dirs):
      qutils.get_price_direction(asset_price_history = asset_price_series[asset_price_series['Ticker']==x], no_of_days = y)
      

def get_rebal_selections:
  
  
