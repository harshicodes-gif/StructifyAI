import psutil

import streamlit as st


def show_metrics():

    c1, c2 = st.columns(2)

    c1.metric(

        "CPU",

        f"{psutil.cpu_percent()} %",

    )

    c2.metric(

        "RAM",

        f"{psutil.virtual_memory().percent} %",

    )