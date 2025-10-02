import streamlit as st
from auth.services import AuthService

st.set_page_config(page_title="JobGenie AI", page_icon="🧞", layout="centered")

# Centered heading
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.subheader("Welcome to JobGenie AI.")
    st.write("Your AI-Powered Job Search Assistant")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Button layout
col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
with col2:
    if st.button("Sign Up", use_container_width=True):
        st.session_state.page = "signup"
with col3:
    if st.button("Login", use_container_width=True):
        st.session_state.page = "login"

# Show content based on selected page
if st.session_state.page == "signup":
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        button = st.form_submit_button('Register')
    if button:
        auth_service = AuthService()
        auth_service.register_user(email, password)

elif st.session_state.page == "login":
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        button = st.form_submit_button('Login')
    if button:
        auth_service = AuthService()
        auth_service.login_user(email, password)

