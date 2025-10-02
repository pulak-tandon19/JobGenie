import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager


load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL", "http://localhost:8000")

cookies = EncryptedCookieManager(
    prefix="jobgenie/",
    password="super-secret-password"  # keep this safe!
)

if not cookies.ready():
    print("reached cookie if")
    st.stop()