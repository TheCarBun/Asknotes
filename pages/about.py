import streamlit as st
from app import load_css
from pathlib import Path
from utils.ui import base_ui

# Base UI
base_ui()

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


# ---- README ----
with open('README.md', 'r', encoding='utf-8') as f:
    readme_text = f.read()

st.title("README")
st.markdown(readme_text)

st.caption("Work In Progress..")