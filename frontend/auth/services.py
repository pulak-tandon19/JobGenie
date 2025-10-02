import streamlit as st
import requests
from streamlit_cookies_manager import EncryptedCookieManager

from config import BASE_API_URL

cookies = EncryptedCookieManager(
    prefix="jobgenie/",
    password="super-secret-password"  # keep this safe!
)

if not cookies.ready():
    st.stop()

class AuthService:
    def register_user(self, email, password):
        payload = {"email": email, "password": password}
        response = requests.post(f"{BASE_API_URL}/auth/register", json=payload)
        if response.status_code == 201:
            st.success("User registered successfully! Please log in.")
        else:
            data = response.json()['detail']
            if isinstance(data, list):
                st.error(str(data[0]['msg']))
            else:
                st.error(str(data))

    def login_user(self, email, password):
        payload = {"email": email, "password": password}
        response = requests.post(f"{BASE_API_URL}/auth/login", json=payload)
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")
            refresh_token = data.get("refresh_token")

            # Save tokens in cookies
            cookies["access_token"] = access_token
            cookies["refresh_token"] = refresh_token
            cookies.save()
            st.success("Login successful!")
        else:
            st.error(response.json()['message'])