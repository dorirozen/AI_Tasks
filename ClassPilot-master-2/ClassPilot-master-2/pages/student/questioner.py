import streamlit as st
from groq import Groq

import generalFunctions as gf
from utils.Prompts import prompts
import json

st.header("Questioner")


# Need to extract data from database
# Get system prompt for model to generate questions
# Get lesson plan content for generating questions
if st.session_state.subject_content == "":
    st.error("No lesson was chosen, please go back to main page")
    st.stop()

keys = gf.get_data_from_path(gf.MAIN_DATA_PATH+gf.SECRET_KEYS)
for key in keys["Keys"]:
    if key["Api Name"] == "ChatGroq":
        chatGroq_key = key["Key"]

# Model init
if chatGroq_key is None:
    print("Error loading the api key")
    client_questioner = None
else:
    client_questioner = Groq(api_key=chatGroq_key)

initial_prompt = prompts.prompt_questioner

if "subject_content" in st.session_state:
    content = gf.get_data_from_path(gf.MAIN_DATA_PATH+gf.LESSON_CONTENT_PATH)
    for subject in content["subjects"]:
        if subject["subject"] == st.session_state.subject_content:
            prompt = initial_prompt + json.dumps(subject)
            system_prompt = {"role": "system", "content": prompt}


    with st.chat_message("assistant"):
        response = client_questioner.chat.completions.create(
            model=st.session_state["model_questioner"],
            messages=[system_prompt, {"role": "user", "content": "give me a question"}],
            max_tokens=2048,
            stream=False
        ).choices[0].message.content
        st.write(response)

#

def main():
    pass


if __name__ == "__main__":
    main()
