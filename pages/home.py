import streamlit as st
from app import load_css
from pathlib import Path

# Base CSS
st.markdown(f'<style>{load_css()}</style>', unsafe_allow_html=True)

current_file = Path(__file__)
css_file = current_file.parent.parent / 'static' / 'home.css'

# CSS for Home Page
if css_file.exists():
    st.markdown(f"""
    <style>
          {load_css(css_file)}
    </style>
""", unsafe_allow_html=True)
else:
    print("home.css not found")

# ---- Navbar ----
with st.container():
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
st.markdown("---")

st.caption("Work In Progress..")