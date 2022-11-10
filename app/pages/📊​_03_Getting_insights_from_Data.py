import streamlit as st
import pandas as pd
import plotly.express as px
from pandasql import sqldf
from utils.class_analytics import insights as ins

st.set_page_config(layout='wide')

@st.cache
def exer(num):
    return ins.exercise(num)

# LAYOUT #
ex1 = st.container()
ex1_1 = st.columns(2)
ex2 = st.container()
ex3 = st.container()
ex4 = st.container()
ex4_1 = st.columns(2,gap='small')

pysqldf=lambda q: sqldf(q,globals())
df = exer(0)

with ex1:
    st.subheader('How are sales going?')
    sales=exer(1)
    #plot#
    fig=px.line(sales,x='date',y='SALES',color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(title_text="<span style='font-size:22px'><b>Sales over time<b></span>",
                        yaxis_title="Amount",
                        xaxis_title="Date",
                        font=dict(size=14),
                        title={
                            'y':0.98,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    fig.update_xaxes(ticks='outside',ticklen=8,color='white')
    fig.update_yaxes(ticks='outside',ticklen=8,color='white')
    st.plotly_chart(fig,use_container_width=True)
    
    with ex1_1[0]:
        top5 = exer(11)
        #plot#
        p1fig= px.pie(top5, values='SALES',names='COUNTRY',color_discrete_sequence=px.colors.qualitative.Prism)
        p1fig.update_traces(marker=dict(line=dict(color='#000000', width=1)),textposition='inside', textinfo='label')
        p1fig.update_layout(title_text="<span style='font-size:22px'><b>Sales distribution in Top 6 countries<b></span>",
                                font=dict(size=14),
                                title={
                                    'y':0.96,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'},
                                showlegend=False)
        st.plotly_chart(p1fig,use_container_width=True)
    
    with ex1_1[1]:
        prod_status = exer(12)
        #plot#
        p2fig = px.pie(prod_status, values='STATUS',names=prod_status.index,color_discrete_sequence=px.colors.qualitative.Prism)
        p2fig.update_traces(marker=dict(line=dict(color='#000000', width=1)),textposition='inside', textinfo='label')
        p2fig.update_layout(title_text="<span style='font-size:22px'><b>Churn rate<b></span>",
                        font=dict(size=14),
                        title={
                            'y':0.96,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                        showlegend=False)
        st.plotly_chart(p2fig,use_container_width=True)
    
    st.markdown(
        '''
        > Sales have improved over time and it can be seen that the month of November is when we sell more products,
        > although they drop drastically afterward, the numbers at the beginning of this year are better compared to previous years.
        > In addition, the churn rate historically has been lower than the 3%.
        '''
    )


with ex2:
    st.subheader('Where do we sell more, and what do we sell in those places?')

    prods = exer(2)
    #plot#
    fig = px.bar(prods,x='COUNTRY',y='SALES',hover_data=['PRODUCTLINE'],color='PRODUCTLINE',color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(title_text="<span style='font-size:22px'><b>Number of products sold distributed by country<b></span>",
                        yaxis_title="Quantity",
                        xaxis_title="Country",
                        font=dict(size=14),
                        title={
                            'y':0.98,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    fig.update_xaxes(ticks='outside',ticklen=8,color='white')
    fig.update_yaxes(ticks='outside',ticklen=8,color='white')
    st.plotly_chart(fig,use_container_width=True)

    st.markdown(
        '''
        > Most of our customers are located in the USA representing almost 50% of them followed by Spain and France
        > to complement the Top 3 most frequent clients. Globally classic cars are the most sold products as well as
        > vintage cars are the second preferred in the United States.
        '''
    )

with ex3:
    st.subheader('How many customers do we have?')
    
    customs = exer(3)
    quant=customs.N_CUSTOMERS.sum()
    st.markdown(f'> Nowadays, the total of clients we have is {quant} and below we can see where they are located.')
    
    #plot#
    dashfig1=px.choropleth(customs,locations='COUNTRY',locationmode='country names',
                    color='N_CUSTOMERS',color_continuous_scale=px.colors.qualitative.Prism,
                    hover_data=['N_CUSTOMERS', 'SALES'])
    dashfig1.update_layout(title_text="<span style='font-size:22px'><b>How our customers are distributed by the world<b></span>",
                        font=dict(size=14),
                        title={
                            'y':0.98,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    st.plotly_chart(dashfig1,use_container_width=True)

with ex4:
    st.subheader('Is there any product line that has decreased sales dramatically during the last year?')
    st.markdown(
        '''
        > In the following visualization, I decided to take classic car sales since they are the most sold products
        > as a reference to define that Trucks and Buses had decreased the most during the last year. The graphic
        > on the right is the same as the one on the left with the difference that we can see all the different product lines.
        '''
    )

    with ex4_1[0]:
        # query to get a dataframe to then plot it #
        query='''
        SELECT  MONTH_ID, YEAR_ID, PRODUCTLINE, SUM(SALES) as sales
        FROM df
        WHERE YEAR_ID >= 2004 and PRODUCTLINE in ('Classic Cars', 'Trucks and Buses')
        GROUP BY PRODUCTLINE, YEAR_ID, MONTH_ID
        ORDER BY ORDERDATE ASC
        '''
        prod_decr=pysqldf(query)
        prod_decr['date']=prod_decr['YEAR_ID'].astype('str')+'-'+prod_decr['MONTH_ID'].astype('str')
        prod_decr.drop(columns=['MONTH_ID','YEAR_ID'],inplace=True)

        #plot#
        fig = px.line(prod_decr,x='date',y='sales',color='PRODUCTLINE')
        fig.update_layout(title_text="<span style='font-size:22px'><b>Product sales which decreased the most<b></span>",
                        yaxis_title="Sales",
                        xaxis_title="Date",
                        font=dict(size=14),
                        title={
                            'y':0.98,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                        hovermode='x unified')
        fig.update_xaxes(ticks='outside',ticklen=8,color='white')
        fig.update_yaxes(ticks='outside',ticklen=8,color='white')
        st.plotly_chart(fig,use_container_width=True)
        
    with ex4_1[1]:
        # query to get a dataframe to then plot it #
        query='''
        SELECT  MONTH_ID, YEAR_ID, PRODUCTLINE, SUM(SALES) as sales
        FROM df
        WHERE YEAR_ID >= 2004
        GROUP BY PRODUCTLINE, YEAR_ID, MONTH_ID
        ORDER BY ORDERDATE ASC
        '''
        prod_decr=pysqldf(query)
        prod_decr['date']=prod_decr['YEAR_ID'].astype('str')+'-'+prod_decr['MONTH_ID'].astype('str')
        prod_decr.drop(columns=['MONTH_ID','YEAR_ID'],inplace=True)
        
        #plot#
        fig = px.line(prod_decr,x='date',y='sales',color='PRODUCTLINE')
        fig.update_layout( yaxis_title="Sales",
                        xaxis_title="Date",
                        font=dict(size=14),
                        title={
                            'y':0.98,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                        hovermode='x unified')
        fig.update_xaxes(ticks='outside',ticklen=8,color='white')
        fig.update_yaxes(ticks='outside',ticklen=8,color='white')
        st.plotly_chart(fig,use_container_width=True)