import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

df = pd.read_csv("Latest Covid-19 India Status.csv")
st.set_page_config(page_title="Covid 19 India Dashboard", page_icon="🦠", layout="wide", initial_sidebar_state="expanded")
st.title(":red[Covid 19] Dashboard For India")
st.markdown('This dashboard will visualize Covid 19 cases in India')
st.markdown('Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.')
st.sidebar.title("Visualization Selector")
st.sidebar.markdown("Select the Charts/Plots accordingly:")
visualization = st.sidebar.selectbox(":red[Visualization type]", ['Bar Plot', 'Pie chart','Line chart', 'Scatter plot'])
states=st.sidebar.multiselect(":red[Select states:]",options=df['State/UTs'].unique(),default=["West Bengal","Maharashtra","Delhi","Gujarat"])
filtered_df=df[df["State/UTs"].isin(states)]
st.subheader(":green[SUMMARY OF THE DATASET]")
total_confirmed=int(filtered_df["Active"].sum())
total_recovered=int(filtered_df["Discharged"].sum())
total_deaths=int(filtered_df["Deaths"].sum())
total_cases=int(filtered_df["Total Cases"].sum())
death_ratio=int(filtered_df["Death Ratio"].sum())
active_ratio=int(filtered_df["Active Ratio"].sum())
discharge_ratio=int(filtered_df["Discharge Ratio"].sum())
col1,col2,col3,col4 = st.columns(4)
col1.metric(":red[Confirmed Cases]",f"{total_confirmed:,}",f"{active_ratio}")
col2.metric(":red[Recovered]",f"{total_recovered:,}",f"{discharge_ratio}")
col3.metric(":red[Deaths]",f"{total_deaths:,}",f"{death_ratio}")
col4.metric(":red[Total Cases]",f"{total_cases}")
metric=st.sidebar.selectbox(":red[Select metric to visualize]",["Active","Deaths","Discharged"])

top5_total = df.sort_values(by='Total Cases', ascending=False).head(5)

# PIE CHART: Top 5 states by total cases
fig_pie = px.pie(top5_total, names='State/UTs', values='Total Cases', title='Top 5 States/UTs by Total COVID-19 Cases')
st.plotly_chart(fig_pie)

# Sort by Deaths and get top 5
top5_deaths = df.sort_values(by='Deaths', ascending=False).head(5)

# BAR CHART: Top 5 states by deaths
fig_bar = px.bar(top5_deaths, x='State/UTs', y='Deaths', 
                 title='Top 5 States/UTs by COVID-19 Deaths', color='Deaths')
fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar)

#Bar Chart
if visualization == 'Bar Plot':
    st.subheader(":green[Bar Plot]")

    # Sort data by the selected metric 
    sort_df = filtered_df.sort_values(metric, ascending=True)
    fig_bar = px.bar(
        sort_df,
        x=metric,
        y='State/UTs',
        orientation='h',
        title=f'{metric.title()} by State',
        color=metric,
        color_continuous_scale='Blues'
    )
    fig_bar.update_layout(
        xaxis_title=metric.title(),
        yaxis_title='State/UTs',
        height=600
    )
    st.plotly_chart(fig_bar)

#Pie chart
if visualization == 'Pie chart':
    st.subheader(":green[Pie Chart]")

    # Sort data by the selected metric 
    sort_df = filtered_df.sort_values(metric, ascending=True)
    fig_pie = px.pie(
        sort_df,
        names='State/UTs',
        values=metric,
        title='Pie Chart of Selected States',
        hole=0,  
    )
    fig_pie.update_traces(textinfo='percent+label', rotation=100)
    st.plotly_chart(fig_pie)

#Line chart
if visualization == 'Line chart':
    st.subheader(":green[Line Chart]")
    sort_df = filtered_df.sort_values(metric, ascending=True)

    fig_line = px.line(
        sort_df,
        x="State/UTs",
        y=metric,
        markers=True,
        title=f"{metric.title()} Across States")
    
    fig_line.update_traces(line=dict(color="firebrick", width=3))
    fig_line.update_layout(
        xaxis_title="State/UTs",
        yaxis_title=metric.title(),
        height=500)

    st.plotly_chart(fig_line)

#Scatter plot
if visualization =='Scatter plot':
    st.subheader(":green[Scatter Plot]")
    sort_df = filtered_df.sort_values(metric, ascending=True)

    fig_scatter = px.scatter(
        sort_df,
        x='Total Cases',             
        y=metric,                   
        color='State/UTs',          
        size=metric,                
        hover_name='State/UTs',
        title=f'{metric.title()} vs Total Cases')
    
    fig_scatter.update_layout(
        xaxis_title='Total Cases',
        yaxis_title=metric.title(),
        height=600)
    st.plotly_chart(fig_scatter)












