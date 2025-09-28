import streamlit as st

# Title
st.title("JobGenie AI Test App")

# User input
name = st.text_input("Enter your name:")
skills = st.text_area("Enter your skills (comma-separated):")

# Button
if st.button("Generate Job Recommendation"):
    if not name or not skills:
        st.warning("Please enter your name and skills!")
    else:
        # Dummy job recommendations
        skill_list = [s.strip() for s in skills.split(",")]
        recommended_jobs = []
        if "Python" in skill_list:
            recommended_jobs.append("Backend Developer at TechCorp")
        if "JavaScript" in skill_list:
            recommended_jobs.append("Frontend Developer at Webify")
        if "AWS" in skill_list:
            recommended_jobs.append("Cloud Engineer at CloudNet")
        
        if recommended_jobs:
            st.success(f"Hi {name}, here are some recommended jobs for you:")
            for job in recommended_jobs:
                st.write(f"- {job}")
        else:
            st.info("No specific matches found. Try adding more skills!")
