import streamlit as st

from components.profile.services import ProfileService
from config import BASE_API_URL

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

st.subheader("👤 My Profile")

profile_service = ProfileService()
profile = profile_service.get_profile()

if profile:
    if not st.session_state.edit_mode:
        # Display profile in read-only mode
        profile_pic_url = profile.get("profile_picture")
        if profile_pic_url:
            profile_pic_url = f"{BASE_API_URL}{profile_pic_url}"
            st.image(profile_pic_url, width=150)
        else:
            st.info("No profile picture uploaded.")
        st.text(f"Email: {profile['email']}")
        st.text(f"First Name: {profile.get('first_name', '')}")
        st.text(f"Last Name: {profile.get('last_name', '')}")
        
        if st.button("✏️ Edit Profile"):
            st.session_state.edit_mode = True

    else:
        # Editable form
        with st.form("edit_profile_form"):
            profile_pic_url = profile.get("profile_picture")
            if profile_pic_url:
                profile_pic_url = f"{BASE_API_URL}{profile_pic_url}"
                st.image(profile_pic_url, width=150)
            uploaded_file = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])

            first_name = st.text_input("First Name", profile.get("first_name", ""))
            last_name = st.text_input("Last Name", profile.get("last_name", ""))

            submitted = st.form_submit_button("💾 Save Changes")
            cancel = st.form_submit_button("❌ Cancel")

            new_url = None
            if uploaded_file:
                new_url = profile_service.upload_picture(uploaded_file)

            if submitted:
                payload = {
                    "first_name": first_name,
                    "last_name": last_name,
                }

                profile_service = ProfileService()

                if new_url:
                    payload["profile_picture"] = new_url

                profile_service.update_profile(payload)   

            if cancel:
                st.session_state.edit_mode = False
