import streamlit as st
import requests

from config import BASE_API_URL, cookies


def make_authorized_request(
    method: str,
    url: str,
    payload: dict = None,
    files=None,
    timeout: int = 10,  # ✅ Default 10 seconds timeout
):
    """
    Makes an API request with access token.
    If token expired (401), refreshes token and retries once.
    Always returns the response.
    """
    access_token = cookies.get("access_token")
    refresh_token = cookies.get("refresh_token")

    headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
    full_url = f"{BASE_API_URL}{url}"

    try:
        # ✅ Send the initial request with timeout
        with st.spinner("Loading... ⏳"):
            response = requests.request(method, full_url, headers=headers, json=payload, files=files, timeout=timeout)
    except:
        st.error("Something went wrong, please try again later!")
        return None

    # ✅ Handle token refresh logic
    if response.status_code == 401 and refresh_token:
        refresh_headers = {"Authorization": f"Bearer {refresh_token}"}
        try:    
            with st.spinner("Loading... ⏳"):
                refresh_resp = requests.get(f"{BASE_API_URL}/auth/refresh_token", headers=refresh_headers, timeout=timeout)
        except:
            st.error("Something went wrong, please try again later!")
            return None

        if refresh_resp.status_code == 200:
            new_token_data = refresh_resp.json()
            new_access_token = new_token_data.get("access_token")

            if new_access_token:
                cookies["access_token"] = new_access_token
                headers["Authorization"] = f"Bearer {new_access_token}"

                try:
                    # ✅ Retry original request once with timeout
                    with st.spinner("Loading... ⏳"):
                        response = requests.request(method, full_url, headers=headers, json=payload, files=files, timeout=timeout)
                except:
                    st.error("Something went wrong, please try again later!")
                    return None
        else:
            st.session_state.show_login_again_msg = True
            st.session_state.page = "login"
            st.switch_page("components/auth/Auth.py")

    return response
