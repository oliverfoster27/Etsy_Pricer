import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
import plotly.express as px
from storage import DataQuery

db = DataQuery()


def app():
    session_names = db.get_sessions()
    if len(session_names) == 0:
        st.write("There are no jobs to analyze")
    elif len(session_names) > 0:
        option = st.selectbox("Which session would you like to analyze?", [f"{x[0]} - '{x[1]}'" for x in session_names])
        bins = st.selectbox("Number of bins", range(10, 101))
        df = db.get_df(option.split(' - ')[0])
        fig = px.histogram(df, x='sale_price', nbins=int(bins))
        st.plotly_chart(fig)
        avg_price = db.get_average_price(option.split(' - ')[0])
        st.write(f'Average Price: ${"%.2f" % avg_price}')
    st.button("Refresh")


