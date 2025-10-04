import streamlit as st
import requests

from config import BASE_API_URL, cookies


class AuthService:
    def register_user(self, email, password):
        payload = {"email": email, "password": password}
        with st.spinner("Loading... ⏳"):
            try:
                response = requests.post(f"{BASE_API_URL}/auth/register", json=payload)
            except:
                st.error("Something went wrong, please try again later!")
                return None
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
        with st.spinner("Loading... ⏳"):
            try:
                response = requests.post(f"{BASE_API_URL}/auth/login", json=payload)
            except:
                st.error("Something went wrong, please try again later!")
                return None
        if response.status_code == 200:
            st.success("Login successful!")

            data = response.json()
            access_token = data.get("access_token")
            refresh_token = data.get("refresh_token")

            # Save tokens in cookies
            cookies["access_token"] = access_token
            cookies["refresh_token"] = refresh_token
            cookies.save()
        else:
            st.error(response.json()['message'])