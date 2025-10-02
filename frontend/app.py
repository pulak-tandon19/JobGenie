import streamlit as st

st.set_page_config(page_title="JobGenie AI", page_icon="🧞", layout="centered")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.title("JobGenie AI")

pg = st.navigation([st.Page("auth/Auth.py"), st.Page("page_1.py"), st.Page("page_2.py")])
pg.run()
