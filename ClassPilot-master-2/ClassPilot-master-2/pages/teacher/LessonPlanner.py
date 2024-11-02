import json
from io import StringIO

import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from groq import Groq
from utils.textExtractors import extractText
from utils.Prompts import prompts

chatGroq_key = None
client_groq = None
# need to input the key in secret_keys from Groq website
with open("utils/data/secret_keys.json") as f:
    keys = json.load(f)["Keys"]
    for key in keys:
        if key["Api Name"] == "ChatGroq":
            chatGroq_key = key["Key"]

# if key not found in data
if chatGroq_key is None:
    print("Error loading the api key")
else:
    client_groq = Groq(api_key=chatGroq_key)
# select the prompt from the Prompts file
system = {"role": "system", "content": prompts.prompt_1}

st.header("Lesson Plan Creating")
st.write(f"You are logged in as {st.session_state.role}.")

# init the model name in session state
if "model_planner" not in st.session_state:
    st.session_state["model_planner"] = "llama3-70b-8192"
# init message history for chat display and model context
if "messages_planner" not in st.session_state:
    st.session_state.messages_planner = []
for message in st.session_state.messages_planner:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# need to append the system prompt for model

if client_groq is not None:
    # init the file upload ui
    file_input = st.file_uploader("Upload the Lesson Summery", accept_multiple_files=True)
    # if file was uploaded, this will activate
    if file_input:
        with st.spinner("Processing"):  # nice ui loading
            file_string = extractText.get_pdf_text(file_input)
            st.session_state.messages_planner.append({"role": "user", "content": file_string})

            with st.chat_message("assistant"):
                messages = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages_planner
                              ]
                messages.append(system)
                response = client_groq.chat.completions.create(
                    model=st.session_state["model_planner"],
                    messages=messages,
                    max_tokens=2048,
                    stream=False
                ).choices[0].message.content
                st.write(response)
            st.session_state.messages_planner.append({"role": "assistant", "content": response})
    # init text chat input ui
    prompt = st.chat_input("Enter the lesson subject")
    if prompt:  # if entered text

        # Add user message to chat history
        st.session_state.messages_planner.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Model processing
        with st.spinner("Processing"):  # nice ui loading
            with st.chat_message("assistant"):
                messages = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages_planner
                              ]
                messages.append(system)
                response = client_groq.chat.completions.create(
                    model=st.session_state["model_planner"],
                    messages=messages,
                    max_tokens=2048,
                    stream=False
                ).choices[0].message.content
                st.write(response)
            st.session_state.messages_planner.append({"role": "assistant", "content": response})


def main():
    pass


if __name__ == "__main__":
    main()
