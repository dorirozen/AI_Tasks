
import streamlit as st

def init():
    # Initialize in session state and default value for values
    if "role" not in st.session_state:
        st.session_state.role = None

    if "subject_content" not in st.session_state:
        st.session_state.subject_content = ""

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"

    if "model_questioner" not in st.session_state:
        st.session_state["model_questioner"] = "llama3-70b-8192"
    # Page Configuration

    st.set_page_config(page_title="ClassPilot AI", page_icon=":rocket:", layout="wide")
    st.title("ClassPilot AI")
    st.logo("images/app_Logo.jpg", icon_image="images/app_Logo.jpg")

