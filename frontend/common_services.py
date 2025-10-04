import streamlit as st
import requests

from config import BASE_API_URL, cookies


def make_authorized_request(method: str, url: str, payload: dict = None, files=None):
    print("reached funcn")
    """
    Makes an API request with access token.
    If token expired (401), refreshes token and retries once.
    Always returns the response.
    """
    access_token = cookies.get("access_token")  # assume stored at login
    refresh_token = cookies.get("refresh_token")

    headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}

    full_url = f"{BASE_API_URL}{url}"

    # Send the initial request
    response = requests.request(method, full_url, headers=headers, json=payload, files=files)

    # If access token expired → try refresh
    if response.status_code == 401 and refresh_token:
        print("reached unauthorized if")
        refresh_headers = {"Authorization": f"Bearer {refresh_token}"}
        refresh_resp = requests.get(f"{BASE_API_URL}/auth/refresh_token", headers=refresh_headers)

        if refresh_resp.status_code == 200:
            print("got new access")
            new_token_data = refresh_resp.json()
            new_access_token = new_token_data.get("access_token")

            if new_access_token:
                # Update token in session
                cookies["access_token"] = new_access_token
                headers["Authorization"] = f"Bearer {new_access_token}"

                # Retry original request once
                response = requests.request(method, full_url, headers=headers, json=payload, files=files)
        else:
            # Refresh token invalid → force logout
            st.session_state.show_login_again_msg = True
            st.session_state.page == "login"
            st.switch_page("components/auth/Auth.py")  # or your login page path

    return response
