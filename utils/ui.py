import streamlit as st

def base_ui():
    st_config()
    with st.container():
        navbar()
    st.markdown("---")


def st_config():
    st.set_page_config(
        page_title="AskNotes.ai", 
        page_icon='📝', 
        layout="wide", 
        initial_sidebar_state='expanded'
    )

def navbar():
    app_col, home_col, about_col = st.columns(3)

    app_col.page_link(
        page='app.py',
        label='App',
        icon=':material/robot_2:'
    )
    home_col.page_link(
        page= "pages/home.py",
        label= "Home",
        icon= ':material/home:'
    )
    about_col.page_link(
        page='pages/about.py',
        label='About',
        icon=':material/star:',
    )

def promo():
    with open("./static/sidebar.html", "r", encoding="UTF-8") as sidebar_file:
        sidebar_html = sidebar_file.read()
    st.html(sidebar_html)