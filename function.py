import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread #-> Để update data lên Google Spreadsheet
from gspread_dataframe import set_with_dataframe #-> Để update data lên Google Spreadsheet
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd
from vnstock import Finance #Báo cáo tài chính
from vnstock import Listing #Thông tin niêm yết
from vnstock import Company #Thông tin công ty 
from vnstock import Company
from vnstock import Quote #Thống kê giá lịch sử
from vnstock import Trading #Bảng giá giao dịch
from vnstock import Screener #Bộ lọc cổ phiếu dung source TCBS

# ------------------------------
USER_CREDENTIALS = st.secrets["USER_CREDENTIALS"] 

def login_screen():
    st.header("Stock Analyze tool is private.")
    st.subheader("Please log in.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        # if  username in st.secrets['user'] and password==st.secrets["passwords"] and username==st.secrets['user']:
        st.balloons()

        if username in USER_CREDENTIALS and password == USER_CREDENTIALS[username]:
            st.session_state.is_logged_in = True
            st.session_state.username = username
            st.rerun()

        else:
            st.error("Invalid username or password")

# interaction with vnstock library

#1.pull all profile symbol
def all_symbols(exchanges):
    symbols= Listing(source= "VCI").symbols_by_exchange()
    symbols_by_exchange=symbols[symbols['exchange'].isin(exchanges)]
    symbolsin=Listing(source= "VCI").symbols_by_industries()
    symbols_industries_by_exchange=symbolsin[symbolsin['symbol'].isin(symbols_by_exchange["symbol"].tolist())]
    return symbols_by_exchange, symbols_industries_by_exchange




def comapny_profile(symbol):
    c=Company(symbol=symbol,source="VCI")
    tbcs=Company(symbol=symbol,source="TCBS")
    profile=c.overview()
    # subsidiary=c.subsidiaries()
    ratio_summary=c.ratio_summary()
    # subsidiaries = c.subsidiaries()
    trading_stats = c.trading_stats()
    dividends = tbcs.dividends()
    if profile is not None and not profile.empty:
        profile['symbol'] = symbol
    if ratio_summary is not None and not ratio_summary.empty:
        ratio_summary['symbol'] = symbol
    # if subsidiaries is not None and not subsidiaries.empty:
    #     subsidiaries['symbol']=symbol
    if trading_stats is not None and not trading_stats.empty:
        trading_stats['symbol']=symbol
    if  dividends is not None and not dividends.empty:
        dividends["symbol"]=symbol
    return profile, ratio_summary,trading_stats,dividends

def quote_history(symbol,start,end):
    print(f"Symbols: {symbol}, Start: {start}, End: {end}")
    print(f"Type(symbols): {type(symbol)}")
    quote = Quote(symbol=symbol, source='VCI')
    print(quote)
    quotehistory=quote.history(start=start, end=end)
    quotehistory['symbol'] = symbol
    intraday = quote.intraday()
    intraday["symbol"]=symbol
    return quotehistory ,intraday


def screener(symbol):
    screener_df = Screener().stock(params={"exchangeName": "HOSE,HNX,UPCOM"}, limit=1700)
    return screener_df
def push_stock(spreadsheet_key,df1,ws1):


    gd.set_with_dataframe(ws1,df1)
    # gd.set_with_dataframe(ws2, df2)
    st.success('Done')

# def pull_profile_symbol():
