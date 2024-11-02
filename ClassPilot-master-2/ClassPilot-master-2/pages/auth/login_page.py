import streamlit as st
import json


def get_user_role(user_name, password):
    f = open("utils/data/users.json")
    data = json.load(f)
    for user in data["users"]:
        if user["userName"] == user_name and user["password"] == password:
            return user["role"]
    return None


st.header("Log In")
user_name_input = st.text_input("User Name")
password_input = st.text_input("Password")
if st.button("Log In") and (user_name_input != "" or password_input != ""):
    role = get_user_role(user_name_input, password_input)
    if role is not None:
        st.session_state.role = role
        st.rerun()


def main():
    pass


if __name__ == "__main__":
    main()
