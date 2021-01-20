import yfinance as yf
import streamlit as st
import base64
from io import BytesIO
import pandas as pd
from googlesearch import search

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'
    return href

def name_convert(name):
    searchval = 'yahoo finance '+name
    link = []
    #limits to the first link
    for url in search(searchval, tld='es', lang='es', stop=1):
        link.append(url)
    print(link)
    link = str(link[0])
    link=link.split("/")
    if link[-1]=='':
        ticker=link[-2]
    else:
        x=link[-1].split('=')
        ticker=x[-1]
    return(ticker)

tickers_input = st.sidebar.text_input("Enter tickers or name here","^HSI")
tickersName = tickers_input.replace(';',',').split(",")
tickers=[]
for kw in tickersName:
	tickers.append(name_convert(kw))
start = st.sidebar.text_input("Start Date","2020-01-01")
end = st.sidebar.text_input("End Date","2021-01-01")

interval = st.sidebar.selectbox("Interval",["1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk","1mo","3mo"],8)
group_by = st.sidebar.radio("group by",["ticker","column"])
prepostChoice = st.sidebar.radio("Include prepost market", ["True","Flase"])

# st.write(tickers)
prepost = True
if prepostChoice == False:
	prepost = False
if tickers != [] or tickers != "" or tickers != None:
	yfDf = yf.download(tickers, start=start,end=end,interval=interval,prepost=prepost,group_by=group_by)


yfDf = yfDf.reset_index()
st.dataframe(yfDf)
st.markdown(get_table_download_link(yfDf),unsafe_allow_html=True)