import tushare as ts
import datetime

if __name__ == '__main__':
    start_date = datetime.datetime.now() - datetime.timedelta(days=365)
    total_df = ts.get_stock_basics()
    total_df = total_df[(total_df['timeToMarket'] < int(start_date.strftime("%Y%m%d"))) & (total_df['timeToMarket'] != 0)]
    total_df['increase'] = ""
    for i in range(len(total_df)):
        # print(total_df.index.values[i])
        single_df = ts.get_hist_data(code=total_df.index.values[i], start=start_date.strftime("%Y-%m-%d"))
        if single_df is not None and not single_df.empty:
            start_value = single_df.iloc[-1]['open']
            end_value = single_df.iloc[0]['close']
            increase = (end_value - start_value) / start_value
            total_df.loc[total_df.index.values[i], 'increase'] = increase
        else:
            pass
        # print(total_df.loc[total_df.index.values[i]])
    total_df = total_df.sort_values(by="increase", ascending=False)
    total_df = total_df.iloc[:int(len(total_df)*0.13)]
    total_df.to_csv('/home/ubuntu/rps_result/'+datetime.datetime.now().strftime("%Y%m%d")+'.csv')
