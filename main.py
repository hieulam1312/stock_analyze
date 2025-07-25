import streamlit as st
from function import login_screen, push_stock,all_symbols,comapny_profile,screener,quote_history
# st.title("Hi there")

from google.oauth2 import service_account
import gspread #-> Để update data lên Google Spreadsheet
from gspread_dataframe import set_with_dataframe #-> Để update data lên Google Spreadsheet
from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials

# Using object notation
import streamlit as st
import gspread as gs
import gspread_dataframe as gd
# ------------------------------
# Configurable credentials


list_symbol = ['TCB',"PAN","HPG"]
list_feature =["Crawing company profiles",
               "Get market price history",
               "Get TCBS measures all stock",
               "Get current market price",
               "Get financial reports"]

# ------------------------------
# Session state check
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# ------------------------------
# Login flow

if not st.session_state.is_logged_in:
    login_screen()
    
else:
    st.sidebar.title("Main feature")
    f=st.sidebar.selectbox("Select feature",options=list_feature)
    st.sidebar.markdown("---")
    if f=="Crawing company profiles":
            #add function here        

        st.sidebar.header("Conformation Selection")
        exchanges = st.sidebar.multiselect(
        "Select Exchange(s)",
        options=['HSX', 'HNX', 'UPCOM'],
        default=['HSX'])
        symbols_by_exchange, symbols_industries_by_exchange = all_symbols(exchanges)
     
        industries=st.sidebar.selectbox(
            "Select industry(es)",
            options=symbols_industries_by_exchange['icb_name3'].tolist())
            # industries_list = symbols_industries_by_exchange['icb_name3'].tolist() if "ALL" in industries  else industries
   
        symbols_by_industry_exchange=symbols_industries_by_exchange[symbols_industries_by_exchange["icb_name3"]==industries]
        symbols=st.sidebar.selectbox(
        "Select symbol(s)",options=symbols_by_industry_exchange["symbol"].tolist())
        # symbols_list = symbols_by_industry_exchange["symbol"].tolist() if "ALL" in symbols else symbols

        profile, ratio_summary,trading_stats,dividends=comapny_profile(symbols)
        st.subheader("Profiles company")
        st.dataframe(profile)

        st.subheader("Ratio summary")
        st.dataframe(ratio_summary)
    if f == "Get market price history":
        st.subheader("market price history")
        st.sidebar.header("Conformation Selection")       
        symbols=st.sidebar.selectbox("Select symbol(s)",options=list_symbol)       
        start_date = st.sidebar.date_input("Start date").strftime('%Y-%m-%d')
        end_date = st.sidebar.date_input("End date").strftime('%Y-%m-%d')
        quotehistory,intraday =quote_history(symbols,start_date,end_date)
        st.subheader("Quote History")
        st.write(quotehistory)
        st.markdown(" ")
        st.subheader("Intraday")
        st.write(intraday)

    if f=="Get TCBS measures all stock":
        st.subheader("Marketprice")
        st.sidebar.header("Conformation Selection")
        symbols=st.sidebar.selectbox("Select symbol(s)",options=list_symbol)
        st.dataframe(screener(symbols))
    # Select exchanges
       








    # --------------------------------##-----------------------------------------------
    # # Using "with" notation
    # with st.sidebar:
 
    # )
    #     


        
    # finance = Finance(symbol='TCB', source='TCBS')

    # income_statement=finance.income_statement(period='year', lang='en')
    # # cashflow = finance.cash
    # # print(income_statement)

    # st.subheader("1. Finance")

    # st.dataframe(income_statement)

    # st.subheader ("2.All companies")
    # st.dataframe(listing)


    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'],
    )
    gc = gspread.authorize(credentials)


    # if st.button("Export Gsheet"):
    #      ws=gc.open('Stock Analyze').worksheet("Company profile")
        #  push_stock(listing,ws)