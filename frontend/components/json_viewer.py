import streamlit as st


def show_json():

    st.json(
        {
            "status": "Waiting",
            "asset": "",
            "issue": "",
            "priority": "",
            "operator": "",
        }
    )
