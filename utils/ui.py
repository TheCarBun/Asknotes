import streamlit as st

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