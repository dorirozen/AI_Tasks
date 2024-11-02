import streamlit as st

if st.button("Log Out?"):
    st.session_state.role = None
    st.rerun()


def main():
    pass


if __name__ == "__main__":
    main()
