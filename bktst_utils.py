from datetime import datetime

def generate_weights(no_of_assets, bktst_strt_dt, bktst_end_dt, rebal_frequency = , weighting_scheme = 'EW'):
  if weighting_scheme == 'EW':
    cons_weights = [1.000000/no_of_assets] * no_of_assets
  
  return cons_weights
