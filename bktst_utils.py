def generate_weights(no_of_assets, bktst_strt_dt, bktst_end_dt, rebal_frequency = '3M', weighting_scheme = 'EW'):
  con_weights = [1.0000/no_of_assets] * no_of_assets
