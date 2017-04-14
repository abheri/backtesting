#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 13:50:22 2017

@author: rishant
"""
import pandas as pd
import pdb
from datetime import datetime
import datetime as dt
import cPickle as pickle 
import numpy
import math as mt

today = str(dt.date(2017,01,02))
name = {5633:'ACC',3861249:'ADANI PORTS',325121:'AMBUJA CEMENTS',60417:'ASIAN PAINTS',70401:'AUROBINDO PHARM',1510401:'AXIS BANK',4267265:'BAJAJ AUTO',1195009:'BANK OF BARODA',2714625:'BHARTI AIRTEL',7458561:'BHARTI INFRATEL',112129:'BHEL',558337:'BOSCH',134657:'BPCL',177665:'CIPLA',5215745:'COAL INDIA',225537:'DR. REDDYS LAB',232961:'EICHER MOTORS',1207553:'GAIL',315393:'GRASIM',1850625:'HCL TECH',340481:'HDFC',341249:'HDFC BANK',345089:'HERO MOTOCORP',348929:'HINDALCO',356865:'HUL',1270529:'ICICI BANK',3677697:'IDEA CELLULAR',1346049:'INDUSIND BANK',408065:'INFOSYS',424961:'ITC',492033:'KOTAK MAHINDRA',2939649:'LARSEN & TOUBRO',2672641:'LUPIN',3400961:'M&M',2815745:'MARUTI SUZUKI',2977281:'NTPC',633601:'ONGC',3834113:'POWER GRID CORP',738561:'RELIANCE',779521:'SBI',857857:'SUN PHARMA',884737:'TATA MOTORS',4343041:' TATA MOTORS DVR',877057:'TATA POWER',895745:'TATA STEEL',2953217:'TCS',3465729:'TECH MAHINDRA',2952193:'ULTRA TECH CEMENT',969473:'WIPRO',3050241:'YES BANK',975873:'ZEE ENTERTAINMENT'}

gap = 0.02
no_constituents=50
no_days = 6
long_cutoff_rank=6
short_cutoff_rank=44
days_rank_lag=1
day_lag=1
buffer_long=0.00
buffer_short=0.000
transaction_cost= 0.0024
stop_loss = 0.05
vol_scaling =0.008
                                                                    df[('OPEN',name[instrument_token])]<df[('Close_lag',name[instrument_token])]),df[('Open_long_buffer_price',name[instrument_token])]<df[('HIGH',name[instrument_token])]),df[('gap',name[instrument_token])] >((-1)* gap))
    
    df[('long_stop_loss',name[instrument_token])]=0#numpy.logical_and(numpy.logical_and(numpy.logical_and(numpy.logical_and(df[('rank_lag',name[instrument_token])]<long_cutoff_rank,
                                                                    #df[('OPEN',name[instrument_token])]<df[('Close_lag',name[instrument_token])]),df[('Open_long_buffer_price',name[instrument_token])]<df[('HIGH',name[instrument_token])]),df[('gap',name[instrument_token])] >((-1)* gap)),df[('OPEN',name[instrument_token])]*(1 - stop_loss)>df[('LOW',name[instrument_token])])
    
    df[('signal_short',name[instrument_token])]=numpy.logical_and(numpy.logical_and(numpy.logical_and(df[('rank_lag',name[instrument_token])]>short_cutoff_rank,
                                                                    df[('OPEN',name[instrument_token])]>df[('Close_lag',name[instrument_token])]),df[('Open_short_buffer_price',name[instrument_token])]>df[('LOW',name[instrument_token])]),df[('gap',name[instrument_token])] < gap)
    
    df[('short_stop_loss',name[instrument_token])]=0#numpy.logical_and(numpy.logical_and(numpy.logical_and(numpy.logical_and(df[('rank_lag',name[instrument_token])]>short_cutoff_rank,
                                                                    #df[('OPEN',name[instrument_token])]>df[('Close_lag',name[instrument_token])]),df[('Open_short_buffer_price',name[instrument_token])]>df[('LOW',name[instrument_token])]),df[('gap',name[instrument_token])] < gap),df[('OPEN',name[instrument_token])]*(1 + stop_loss)<df[('HIGH',name[instrument_token])])
    
    df[('stop_loss_pnl_long',name[instrument_token])]=df[('long_stop_loss',name[instrument_token])]*(-1)* stop_loss
    df[('stop_loss_pnl_short',name[instrument_token])]=df[('short_stop_loss',name[instrument_token])]*(-1)* stop_loss
    df[('pnl_long',name[instrument_token])]=(df[('signal_long',name[instrument_token])]*(df[('intraday_returns',name[instrument_token])]-buffer_long-transaction_cost)*(1-df[('long_stop_loss',name[instrument_token])]) + df[('stop_loss_pnl_long',name[instrument_token])]*df[('long_stop_loss',name[instrument_token])])*df[('Leverage',name[instrument_token])]
    df[('pnl_short',name[instrument_token])]=(df[('signal_short',name[instrument_token])]*((-1)*df[('intraday_returns',name[instrument_token])]-buffer_short-transaction_cost)*(1-df[('short_stop_loss',name[instrument_token])]) + df[('stop_loss_pnl_short',name[instrument_token])]*df[('short_stop_loss',name[instrument_token])])*df[('Leverage',name[instrument_token])]
    df[('Net_pnl_long','Net_pnl_long')]=df[[('pnl_long',name[instrument_token])for instrument_token in name]].sum(axis=1)
    df[('Net_pnl_short','Net_pnl_short')]=df[[('pnl_short',name[instrument_token])for instrument_token in name]].sum(axis=1)
    df[('Net_pnl','Net_pnl')]=df[[('Net_pnl_short','Net_pnl_short'),('Net_pnl_long','Net_pnl_long')]].sum(axis=1)
    
df['Index'][0]=100   
for i in range(1,len(df)):
            
            df['Index'][i]=df['Index'][i-1]*(1 + float(df[('Net_pnl','Net_pnl')][i]/no_constituents))

start_date = 0
end_date = len(df)- 1          
sharpe = mt.sqrt(252)*df[('Net_pnl_short','Net_pnl_short')].mean()/df[('Net_pnl_short','Net_pnl_short')].std()
series = (pd.expanding_max(df['Index'][start_date:end_date])-df['Index'][start_date:end_date])/df['Index'][start_date:end_date]            
drawdown = series.max()


def annualised_return(df,start_date,end_date):
            num_years = float(end_date - start_date)/252
            num_years_inv = float(1)/num_years
            #pdb.set_trace()
            ratio_final_initial = df['Index'][end_date]/df['Index'][start_date]
            annualised_return = mt.pow(ratio_final_initial,num_years_inv)-1
            return annualised_return
            
annualised = annualised_return(df,start_date,end_date)      
print sharpe,drawdown,annualised