import pandas as pd
import datetime
import os

today = datetime.datetime.now().strftime("%Y%m%d")
yesterday = os.popen("ls -l /home/ubuntu/rps_result/|tail -2|awk 'FNR==1 {print $9}'").readlines()[0].strip()
stock_df = pd.read_csv('/home/ubuntu/rps_result/'+today+'.csv')
stock_df = stock_df.loc[(stock_df['totalAssets']<2000000) & (stock_df['rev']>50) & (stock_df['profit']>50)]
old_stock_df = pd.read_csv('/home/ubuntu/rps_result/'+yesterday)
stock_df = stock_df[~stock_df['name'].isin(old_stock_df['name'])]
stock_df.to_csv('/home/ubuntu/email/new_focus.csv')

os.system('cat /home/ubuntu/email/rps_main.txt>>/home/ubuntu/email/'+today+'.txt')
os.system('cat /home/ubuntu/email/new_focus.csv>>/home/ubuntu/email/'+today+'.txt')
os.system("/usr/sbin/ssmtp wuxudong25@gmail.com < /home/ubuntu/email/"+today+'.txt')
