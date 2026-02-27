import streamlit as st
import yfinance as yf
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

st.title("Financial Systemic Risk Contagion Engine")

# Step 1: Select stocks

stocks = st.multiselect(

"Select Assets",

['RELIANCE.NS','HDFCBANK.NS','ICICIBANK.NS','INFY.NS','TCS.NS','SBIN.NS'],

default=['RELIANCE.NS','HDFCBANK.NS','ICICIBANK.NS']

)

if len(stocks) > 1:

    # Step 2: Download data
    
    data = yf.download(stocks, period="6mo")['Close']

    returns = data.pct_change().dropna()

    corr = returns.corr()

    st.subheader("Correlation Matrix")

    st.dataframe(corr)

    # Step 3: Create network

    G = nx.Graph()

    threshold = st.slider("Correlation Threshold",0.0,1.0,0.5)

    for stock in corr.columns:

        G.add_node(stock)

    for i in corr.columns:

        for j in corr.columns:

            if i != j and corr[i][j] > threshold:

                G.add_edge(i,j)

    pos = nx.spring_layout(G)

    # Step 4: Plot network

    edge_x=[]
    edge_y=[]

    for edge in G.edges():

        x0,y0=pos[edge[0]]

        x1,y1=pos[edge[1]]

        edge_x.extend([x0,x1,None])

        edge_y.extend([y0,y1,None])

    edge_trace=go.Scatter(

        x=edge_x,y=edge_y,

        mode='lines'

    )

    node_x=[]
    node_y=[]
    text=[]

    for node in G.nodes():

        x,y=pos[node]

        node_x.append(x)

        node_y.append(y)

        text.append(node)

    node_trace=go.Scatter(

        x=node_x,

        y=node_y,

        mode='markers+text',

        text=text,

        textposition="top center",

        marker=dict(size=20)

    )

    fig=go.Figure(data=[edge_trace,node_trace])

    st.subheader("Risk Contagion Network")

    st.plotly_chart(fig)

else:

    st.warning("Select at least 2 stocks")



st.title("Financial Contagion Engine")

stocks=['RELIANCE.NS','HDFCBANK.NS','ICICIBANK.NS','INFY.NS','TCS.NS']

data=yf.download(stocks,period="6mo")['Close']

returns=data.pct_change().dropna()

corr=returns.corr()

shock_stock=st.selectbox(

"Select asset to simulate shock",

stocks

)

shock=st.slider(

"Shock magnitude (%)",

-10,-1,-5

)

risk={}

for stock in stocks:

    risk[stock]=corr[shock_stock][stock]*abs(shock)

G=nx.Graph()

for stock in stocks:

    G.add_node(stock)

for i in stocks:

    for j in stocks:

        if corr[i][j]>0.5 and i!=j:

            G.add_edge(i,j)

pos=nx.spring_layout(G)

node_x=[]
node_y=[]
text=[]
size=[]

for node in G.nodes():

    x,y=pos[node]

    node_x.append(x)

    node_y.append(y)

    text.append(node)

    size.append(risk[node]*5)

node_trace=go.Scatter(

x=node_x,

y=node_y,

mode='markers+text',

text=text,

marker=dict(size=size)

)

fig=go.Figure(data=[node_trace])

st.plotly_chart(fig)

st.subheader("Risk Levels")

st.write(risk)


