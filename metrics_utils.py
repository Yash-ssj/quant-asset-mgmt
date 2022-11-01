import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt

def download_ticker_data(ticker_list, start_date, end_date):
    x = 0
    for i in ticker_list:
        print(i+","+str(x))
        ticker_data = yf.download(i, start_date, end_date)
        ticker_data['Ticker'] = i
        if x==0:
            ticker_data_consolidated = pd.DataFrame(columns=ticker_data.columns.tolist())
        ticker_data_consolidated = ticker_data_consolidated.append(ticker_data)
        x = x+1
        
    ticker_data_consolidated = ticker_data_consolidated.reset_index()
    ticker_data_consolidated.columns = ['Date','Open','High','Low','Close','Adj Close','Volume','Ticker']
    ticker_data_consolidated['Date'] = pd.to_datetime(ticker_data_consolidated['Date'], format = '%Y-%m-%d')
    
    return ticker_data_consolidated
  
def calc_annualized_return(asset_price_history, start_date, end_date = np.NaN):
    x = asset_price_history[asset_price_history['Date']>=start_date].index.to_list()[0]
    if end_date==np.NaN:
        end_date = asset_price_history.loc[len(asset_price_history)-1]['Date']
    y = sorted(asset_price_history[asset_price_history['Date']<=end_date].index.to_list(),reverse=True)[0]
    difference_in_years = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).total_seconds()/(24*60*60*365)
    
    return ((asset_price_history.loc[y]['Close']/asset_price_history.loc[x]['Close'])**(1/difference_in_years)-1)*100.00, ((asset_price_history.loc[y]['Close']/asset_price_history.loc[x]['Close']) - 1) * 100.00 
  
def get_drawdown(asset_price_history, start_date, end_date = np.NaN):
    if end_date==np.NaN:
        end_date = asset_price_history.loc[len(asset_price_history)-1]['Date']
    asset_price_history_truncated = asset_price_history[(asset_price_history['Date']>=start_date) & (asset_price_history['Date']<=end_date)]
    
    asset_price_history_truncated['PrevPeak'] = np.NaN
    for i in asset_price_history_truncated.index:
        asset_price_history_truncated.loc[i,'PrevPeak'] = asset_price_history_truncated[:i+1]['Close'].max()
    asset_price_history_truncated['Drawdown'] = (asset_price_history_truncated['Close']-asset_price_history_truncated['PrevPeak'])/asset_price_history_truncated['PrevPeak']
    
    return asset_price_history_truncated

def plot_price_history(asset_price_history, start_date, end_date):
    annualized_return, actual_return = calc_annualized_return(asset_price_history, start_date, end_date)
    plt.figure(figsize=(20,10))
    plt.plot(asset_price_history[(asset_price_history['Date']>=start_date) & (asset_price_history['Date']<=end_date)]['Date'],asset_price_history[(asset_price_history['Date']>=start_date) & (asset_price_history['Date']<=end_date)]['Close'], label = str(annualized_return) + ", " + str(actual_return))
    plt.legend()

def plot_drawdown(asset_price_history, start_date, end_date = np.NaN):
    asset_dd_history = get_drawdown(asset_price_history, start_date, end_date)
    plt.figure(figsize=(20,10))
    plt.plot(asset_dd_history['Date'], asset_dd_history['Drawdown'], label = 'Max Drawdown = ' & ' + str(asset_dd_history['Drawdown'].max()))
    plt.legend()

def get_price_direction(asset_price_history, no_of_days = 10, end_date = np.NaN):
    if end_date==np.NaN:
        end_date = asset_price_history.loc[len(asset_price_history)-1]['Date']
    asset_price_history_truncated = asset_price_history[asset_price_history['Date']<=end_date]
    if asset_price_history_truncated.loc[-1]['Close']>asset_price_history_truncated.loc[-1].shift(no_of_days)['Close']:
        return 1
    else if asset_price_history_truncated.loc[-1]['Close']==asset_price_history_truncated.loc[-1].shift(no_of_days)['Close']:
        return 0
    else:
        return -1

             
