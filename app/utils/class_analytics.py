import pandas as pd

class insights():
    
    def read(csv):
        return pd.read_csv(csv,encoding='Latin-1')

    def exercise(number):
        df = insights.read('sales_data_sample.csv')
        df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])

        if number == 0: return df
        elif number == 1:
            sales = df[['YEAR_ID','MONTH_ID','SALES']].groupby(['YEAR_ID','MONTH_ID']).agg({'SALES':'sum'})
            sales.reset_index(inplace=True)
            sales['date']=sales['YEAR_ID'].astype('str')+'-'+sales['MONTH_ID'].astype('str')
            sales.drop(columns=['YEAR_ID','MONTH_ID'],inplace=True)
            return sales
        elif number == 11:
            top5 = df[['COUNTRY','SALES']]
            top5 = top5.groupby('COUNTRY').agg({'SALES':'sum'}).sort_values('SALES',ascending=False)
            top5 = top5[:6]
            top5.reset_index(inplace=True)
            return top5
        elif number == 12:
            return  df[['STATUS']].groupby('STATUS').agg({'STATUS':'count'})
        elif number == 2:
            prods = df[['COUNTRY','PRODUCTLINE','SALES']].groupby(['COUNTRY','PRODUCTLINE']).agg({'SALES':'count'})
            prods.reset_index(inplace=True)
            return prods    
        elif number == 3:
            customs = df[['COUNTRY','CUSTOMERNAME','SALES']].groupby('COUNTRY').agg({'CUSTOMERNAME':'nunique','SALES':'sum'})
            customs.reset_index(inplace=True)
            customs.rename(columns={'CUSTOMERNAME':'N_CUSTOMERS'},inplace=True)
            return customs