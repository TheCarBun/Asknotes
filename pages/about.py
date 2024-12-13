import streamlit as st
from app import load_css
from pathlib import Path

# Base CSS
st.markdown(f'<style>{load_css()}</style>', unsafe_allow_html=True)

current_file = Path(__file__)
css_file = current_file.parent.parent / 'static' / 'about.css'

# CSS for About Page
if css_file.exists():
    st.markdown(f"""
    <style>
          {load_css(css_file)}
    </style>
""", unsafe_allow_html=True)
else:
    print("about.css not found")

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

# ---- README ----
with open('README.md', 'r', encoding='utf-8') as f:
    readme_text = f.read()

st.title("README")
st.markdown(readme_text)

st.caption("Work In Progress..")