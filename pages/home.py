import streamlit as st
from app import load_css
from pathlib import Path
from utils.ui import base_ui

# ---- Base UI ----
base_ui()

# Base CSS
st.markdown(f'<style>{load_css()}</style>', unsafe_allow_html=True)

current_file = Path(__file__)
css_file = current_file.parent.parent / 'static' / 'home.css'
html_file = current_file.parent.parent / 'static' / 'home.html'


# HTML for Home Page
st.markdown("""
# ✨Asknotes.ai
### AI teacher that helps you understand your notes
            """)

# CSS for Home Page
if css_file.exists():
    st.markdown(f"""
    <style>
          {load_css(css_file)}
    </style>
""", unsafe_allow_html=True)
else:
    print("home.css not found")

st.link_button(
    label="Try for free :material/arrow_right_alt:",
    url="https://asknotes.streamlit.app/",
    type="primary"
    )

st.markdown("---")
st.image("https://imgur.com/Z4FhMyg.png")