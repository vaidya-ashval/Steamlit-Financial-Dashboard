#==============================================================================
# Initiating
#==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
pd.options.plotting.backend = "plotly"


#==============================================================================
# Tab 1: Summary
#==============================================================================

def tab1():
    
    # Add dashboard title and description
    st.title("Financial dashboard")
    
    st.header('Company profile')
    st.write("-------------------------------------------------------------------------")
    
    tick = yf.Ticker(ticker)

    df = tick.history(start=start_date, end=end_date)
    #Reseting the index
    df = df.reset_index()
    #Converting the datatype to float
    for i in ['Open', 'High', 'Close', 'Low']:
        df[i] = df[i].astype('float64')
    
    
    # Add table to show stock data
    @st.cache
    def GetCompanyInfo(ticker):
        return yf.Ticker(ticker).info
    
    if ticker != '':
        # Get the company information in list format
        info = GetCompanyInfo(ticker)
        
        #initilize ticker 
        tick = yf.Ticker(ticker)

        # Show the company description
        st.image(info['logo_url'])
        
        # Show some statistics
        st.write('**Key Statistics**')
        keys1= ['previousClose', 'open', 'bid', 'ask', 'marketCap', 'volume']
        keys2= ['previousClose', 'open', 'bid', 'ask', 'marketCap', 'volume']
       
        #keys2 = ['previousClose', 'open', 'bid', 'ask', 'marketCap', 'volume']
        company_stats1 = {}  # Dictionary
        company_stats2 = {}
        for key in keys1:
            company_stats1.update({key:info[key]})
        company_stats1 = pd.DataFrame({'Value':pd.Series(company_stats1)})  # Convert to DataFrame
        
        for key in keys2:
            company_stats2.update({key:info[key]})
        company_stats2 = pd.DataFrame({'Value':pd.Series(company_stats2)})
        
        col1, col2 = st.columns(2)
        
        with col1:
           #st.image("https://static.streamlit.io/examples/cat.jpg")
           col1.dataframe(company_stats1)
        
        with col2:
           #st.image("https://static.streamlit.io/examples/dog.jpg")
           col2.dataframe(company_stats2)

        
        st.write("-------------------------------------------------------------------------")
        st.write('**Stock Trend**')

        #st.image("https://static.streamlit.io/examples/owl.jpg")
        fig = go.Figure([go.Scatter(x=df['Date'], y=df['Close'])])
    # =============================================================================
    #            fig = go.Figure([go.Scatter(x=df['Date'], y=df['Close'])])
    # =============================================================================
    # =============================================================================
    #            fig = go.Figure([go.Scatter(x=df1['A'], y=df1['B'])])
    # =============================================================================
    
           #fig.update_layout(title = tick.info['shortName'] + " Share Price", yaxis_title = "Stock Price")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("-------------------------------------------------------------------------")
 
        st.write('**Business Summary:**')
        st.write(info['longBusinessSummary'])
           
        st.write("-------------------------------------------------------------------------")
        
        
        st.write("**Stake Holders**")
        st.write("Major Stake Holders")
        tick.major_holders
        st.write("Institutional Stake Holders")
        tick.institutional_holders
        
    
        
      


#==============================================================================
# Tab 2: Chart
#==============================================================================
## ALL References 
#For creating slider graphs using plotly and yfinance    
#https://towardsdatascience.com/downloading-stock-data-and-representing-it-visually-6433f7938f98
    
#Avoid opening graphs in
# https://github.com/streamlit/streamlit/issues/3622



def tab2():
    
    # Add dashboard title and description
    st.title("Graphs and Visualizations")
    st.write(ticker)
    
    tick = yf.Ticker(ticker)

    df = tick.history(start=start_date, end=end_date)
    
    #Reseting the index
    df = df.reset_index()
    #Converting the datatype to float
    for i in ['Open', 'High', 'Close', 'Low']:
        df[i] = df[i].astype('float64')
    
    graph_type = st.radio('Graph Type',['Line','Candle','OHLC','Area'])

    
    if graph_type == 'Line':
        fig = go.Figure([go.Scatter(x=df['Date'], y=df['Close'])])
        
        fig.update_layout(title = tick.info['shortName'] + " Share Price", yaxis_title = "Stock Price")
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month",                                        
                          stepmode="backward"),
                    dict(count=3, label="3m", step="month",                                        
                          stepmode="backward"),
                    dict(count=6, label="6m", step="month",  
                          stepmode="backward"),
                    dict(count=1, label="YTD", step="year", 
                          stepmode="todate"),
                    dict(count=1, label="1y", step="year", 
                          stepmode="backward"),
                    dict(count=3, label="3y", step="year", 
                          stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    elif graph_type == 'Candle':
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month",                                        
                          stepmode="backward"),
                    dict(count=3, label="3m", step="month",                                        
                          stepmode="backward"),
                    dict(count=6, label="6m", step="month",  
                          stepmode="backward"),
                    dict(count=1, label="YTD", step="year", 
                          stepmode="todate"),
                    dict(count=1, label="1y", step="year", 
                          stepmode="backward"),
                    dict(count=3, label="3y", step="year", 
                          stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    elif graph_type == 'OHLC':
        fig = go.Figure(data=go.Ohlc(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']))
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month",                                        
                          stepmode="backward"),
                    dict(count=3, label="3m", step="month",                                        
                          stepmode="backward"),
                    dict(count=6, label="6m", step="month",  
                          stepmode="backward"),
                    dict(count=1, label="YTD", step="year", 
                          stepmode="todate"),
                    dict(count=1, label="1y", step="year", 
                          stepmode="backward"),
                    dict(count=3, label="3y", step="year", 
                          stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        st.plotly_chart(fig, use_container_width=True)


    

    elif graph_type == 'Area':
        fig = px.area(df, x=df["Date"], y=df["Close"])
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month",                                        
                          stepmode="backward"),
                    dict(count=3, label="3m", step="month",                                        
                          stepmode="backward"),
                    dict(count=6, label="6m", step="month",  
                          stepmode="backward"),
                    dict(count=1, label="YTD", step="year", 
                          stepmode="todate"),
                    dict(count=1, label="1y", step="year", 
                          stepmode="backward"),
                    dict(count=3, label="3y", step="year", 
                          stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        st.plotly_chart(fig, use_container_width=True)


#==============================================================================
# Tab 3: Financials
#==============================================================================

def tab3():
    
        tick = yf.Ticker(ticker)
        
        st.title("Financial Reports")
        left,right = st.columns(2)
        with left:
            ReportType = st.selectbox('Type of Financial Report:',['Income Statement','Balance Sheet','Cash Flow']) 
            PeriodDict = {'Report':['Annual','Quarterly'],'ReportCode':[True,False]}
            PeriodDF=pd.DataFrame(PeriodDict)
        with right:    
            PeriodType = st.radio('Report:',PeriodDF['Report']) #radio to select report period
            

        def reportDisplay(ReportType,PeriodType):
            if ReportType == "Income Statement":
                if PeriodType == False:
                    table = tick.financial
                else: 
                    table = tick.quarterly_financials 
                    
            if ReportType == "Balance Sheet":
                 if PeriodType == False:
                     table = tick.balance_sheet
                 else: 
                     table = tick.quarterly_balance_sheet  
                     
            if ReportType == "Cash Flow":
                if PeriodType == False:
                    table = tick.cashflow
                else: 
                    tick.quarterly_cashflow
                    
            return st.dataframe(table)        



        reportDisplay(ReportType, PeriodType)
                
                
                
            
        

    


#==============================================================================
# Tab 4: Monte Carlo simulation
#==============================================================================
#Reference - ClassNotes Section 3 

def tab4():
    
    st.title("Monte Carlo Simulation")
    
    left,right = st.columns(2)
    with left:
        simulations = st.selectbox('Number of simulations',[200,500,1000])
    with right:    
        horizon = st.selectbox('Time horizon',[30,60,90])
    
    tick = yf.Ticker(ticker)
    stock_price = tick.history(start = start_date, end = end_date)
    
    ### STEP 1
    # Take the close price
    close_price = stock_price['Close']
    
    # The returns ((today price - yesterday price) / yesterday price)
    daily_return = close_price.pct_change()
    
    # The volatility (high value, high risk)
    daily_volatility = np.std(daily_return)

    
    ### STEP 2 - Setup the Monte Carlo Simulation
    np.random.seed(123)
    # Run the simulation
    simulation_df = pd.DataFrame()
    
    for i in range(simulations):
        
        # The list to store the next stock price
        next_price = []
        
        # Create the next stock price
        last_price = close_price[-1]
        
        for j in range(horizon):
            # Generate the random percentage change around the mean (0) and std (daily_volatility)
            future_return = np.random.normal(0, daily_volatility)
    
            # Generate the random future price
            future_price = last_price * (1 + future_return)
    
            # Save the price and go next
            next_price.append(future_price)
            last_price = future_price
        
        # Store the result of the simulation
        next_price_df = pd.Series(next_price).rename('sim' + str(i))
        simulation_df = pd.concat([simulation_df, next_price_df], axis=1)

    #Plot the Graph
        # Plot the simulation stock price in the future
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 10, forward=True)
    
    plt.plot(simulation_df)
    plt.title('Monte Carlo simulation for AAPL stock price')
    plt.xlabel('Day')
    plt.ylabel('Price')
    
    plt.axhline(y=close_price[-1], color='black')
    plt.legend(['Current stock price is: ' + str(np.round(close_price[-1], 2))])
    ax.get_legend().legendHandles[0].set_color('black')
    
    st.plotly_chart(fig, use_container_width=True)
    
#==============================================================================
# Tab 5: Others
#==============================================================================

def tab5():
    
    return None

#==============================================================================
# Main body
#==============================================================================

def run():
    
    # Add the ticker selection on the sidebar
    # Get the list of stock tickers from S&P500
    ticker_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']
    
    
    #st.sidebar.image("https://www.istockphoto.com/es/foto/bull-and-bear-sobre-los-precios-del-mercado-burs%C3%A1til-gm1155610132-314657555?phrase=stock")
    
    st.sidebar.header("Pick your Stock")
    
    # Add selection box
    global ticker
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list)
    
    # Add select begin-end date
    global start_date, end_date
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("Start date", datetime.today().date() - timedelta(days=30))
    end_date = col2.date_input("End date", datetime.today().date())
    
    # Add a radio box
    select_tab = st.sidebar.radio("Select tab", ['Company profile', 'Chart','Financials','Monte Carlo Simulation','Others'])
    
    # Show the selected tab
    if select_tab == 'Company profile':
        # Run tab 1
        tab1()

    elif select_tab == 'Chart':
        # Run tab 2
        tab2()
        
    elif select_tab == 'Financials':
        # Run tab 3
        tab3()
    
    elif select_tab == 'Monte Carlo Simulation':
        # Run tab 4
        tab4()
        
    elif select_tab == 'Others':
        # Run tab 4
        tab5()
        


if __name__ == "__main__":
    run()
    





















