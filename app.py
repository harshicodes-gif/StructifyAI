import streamlit as st

from backend.database.sqlite import initialize_database
from frontend.styles import apply_theme
from frontend.components.navbar import show_navigation

from frontend.pages.home import show_home
from frontend.pages.upload import show_upload
from frontend.pages.history import show_history
from frontend.pages.settings import show_settings

st.set_page_config(
    page_title="Structify AI",
    page_icon="🤖",
    layout="wide",
)

apply_theme()
initialize_database()

page = show_navigation()

if page == "Home":
    show_home()

elif page == "Upload":
    show_upload()

elif page == "History":
    show_history()

else:
    show_settings()