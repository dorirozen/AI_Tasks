import click
import streamlit as st
import pandas as pd
import generalFunctions as gf



student_data = gf.get_data_from_path(gf.MAIN_DATA_PATH+gf.STUDENT_DATA_PATH)

finished_lesson = gf.get_finished_subjects()

df = pd.DataFrame({
    "Main Subject": [subject_content["subject"] for subject_content in finished_lesson["subjects"]],
    "Link Lesson": ['Start Lesson' for _ in finished_lesson["subjects"]],
})

st.header("Lesson Requester")
st.write(f"You are logged in as {st.session_state.role}.")

for index, row in df.iterrows():
    col1, col2 = st.columns([1,5])
    with col1:
        st.write(row["Main Subject"].capitalize())
    with col2:
        if st.button(row["Link Lesson"], key=f"lesson{index}"):
            if "subject_content" not in st.session_state:
                st.session_state.subject_content = "Python"
            st.session_state.subject_content = row["Main Subject"]
            st.switch_page("pages/teacher/TeacherLessonPresenter.py")


def main():
    pass


if __name__ == "__main__":
    main()
