import streamlit as st
from app import add_to_log


def load_css() -> str:
    """
    Loads CSS stylesheet and SVG background from local files.

    Returns:
    - str: The content of the CSS file.
    """
    # Load CSS stylesheet
    try:
        with open('static/styles.css') as f:
            custom_css = f.read()
        return custom_css
    except FileNotFoundError:
        add_to_log("❗Error loading stylesheet: File not found.", "error")
    except Exception as e:
        add_to_log("❗Error loading stylesheet.", "error")


# Custom CSS
st.markdown(f'<style>{load_css()}</style>', unsafe_allow_html=True)


# Hide Sidebar
st.markdown("""
    <style>
        .stSidebar{
            display:none;
            }
                
        .st-emotion-cache-13ln4jf{
            width: 70%;
            max-width: 100%;
            padding: 0;
            }  
    </style>
""", unsafe_allow_html=True)

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