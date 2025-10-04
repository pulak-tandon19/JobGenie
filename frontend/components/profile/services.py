import streamlit as st
import requests
from config import BASE_API_URL, cookies
from common_services import make_authorized_request

class ProfileService():

    def __init__(self):
        if cookies.ready():
            ACCESS_TOKEN = cookies.get("access_token")  # assume stored at login
        else:
            st.stop()

        self.headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    def get_profile(self):
        response = requests.get(f"{BASE_API_URL}/auth/users/me", headers=self.headers)
        response = make_authorized_request("GET", "/auth/users/me")
        return response.json()
    
    def upload_picture(self, file):
        files = {"file": (file.name, file, file.type)}
        response = requests.post(f"{BASE_API_URL}/auth/upload-profile-picture", headers=self.headers, files=files)
        if response.status_code == 200:
            return response.json().get("url")
        else:
            st.error("Failed to upload profile picture.")
            return None
    
    def update_profile(self, payload):
        # response = requests.patch(f"{BASE_API_URL}/auth/users/me", headers=self.headers, json=payload)
        response = make_authorized_request("PATCH", "/auth/users/me", payload=payload)
        if response.status_code == 200:
            st.success("Profile updated successfully!")
            st.session_state.edit_mode = False
        else:
            st.error(str(response.json()))  