import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker
# from matplotlib.backends.backend_pdf import PdfPages 
import requests 
import io 
from datetime import date 



#a list containing the links you want to download from (they must be in csv form)

relevant_data = ["https://www.ons.gov.uk/generator?format=csv&uri=/economy/nationalaccounts/balanceofpayments/timeseries/l87s/mret",
                 "https://www.ons.gov.uk/generator?format=csv&uri=/economy/nationalaccounts/balanceofpayments/timeseries/l87u/mret",
                 "https://www.ons.gov.uk/generator?format=csv&uri=/economy/nationalaccounts/balanceofpayments/timeseries/l87m/mret",
                 "https://www.ons.gov.uk/generator?format=csv&uri=/economy/nationalaccounts/balanceofpayments/timeseries/l87o/mret"]
date_today = date.today()


chart_or_download = input("Do you want chart/s or a download? (C for chart/s, D for Download)")
interval = input("What interval step would you like? (M for monthly, Q for quarterly, Y for yearly)")

for link in relevant_data:

    response = requests.get(link).content
    df = pd.read_csv(io.StringIO(response.decode('utf-8'))) 

    name_of_series = df.columns[1]
    print(name_of_series)
    
    #Removing Headers 
    df = df.iloc[7:]

    #Building Quarterly Dataset 
    is_Quarterly = df['Title'].str.contains('Q')
    Quarterly_df = df[is_Quarterly]
    
    #Building Monthly Dataset 
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    pattern = '|'.join(months)
    is_Monthly = df['Title'].str.contains(pattern)
    Monthly_df = df[is_Monthly]

    #Building Yearly Dataset 
    Yearly_df = df[~is_Monthly & ~is_Quarterly]

    if interval == "Y":
        data = Yearly_df
        chart_interval = "Year"
    elif interval == "M":
        data = Monthly_df
        chart_interval = "Month"
    elif interval == "Q":
        data = Quarterly_df
        chart_interval = "Quarter"
    
    if chart_or_download == "C":
        fig, ax = plt.subplots(1,1)
        ax.plot(data['Title'], pd.to_numeric(data[name_of_series]))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
        plt.title(name_of_series)
        plt.xlabel(chart_interval)
    
    if chart_or_download == "D":  
        try:
            download_df[f'{name_of_series}'] = data[f'{name_of_series}']
        except NameError:
            download_df = data
            download_df = download_df.rename(columns = {'Title' : 'Interval'})
        

if chart_or_download == "C":
    plt.show()

if chart_or_download == "D":
    download_df.to_csv(f'{date_today}_ONS_download.csv', index=False)

    


            










