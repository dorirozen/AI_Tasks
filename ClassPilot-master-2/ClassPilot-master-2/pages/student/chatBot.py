import streamlit as st
import json
from utils.TextToVoice.TextToVoice import TextToVoice

from utils.Prompts import prompts
from pages.student.chatbot.ChatBot import ChatBot

def json_to_text(json_content):
    complete_text = f"Subject: {json_content['subject']} \n"
    for lesson in json_content["lessons"]:
        complete_text += f"Lesson Title: {lesson['title']} \n"
        for page in lesson["pages"]:
            complete_text += f"Subtitle: {page['title']} \n content: {page['content']}\n"
    return complete_text

# Initialize role in session state and default value for role
if "role" not in st.session_state:
    st.session_state.role = "Student"  # default role is Student

if "chat_finished" not in st.session_state:
    st.session_state.chat_finished = False  # default value for chat finished status

st.header("Chatbot")
if "subject_content" not in st.session_state or st.session_state.subject_content == "":
    st.error("No lesson was chosen, please go back to main page")
    st.stop()

# Load lesson text if not already loaded
if "text_lesson" not in st.session_state:
    with open("utils/data/lesson_content.json", "r", encoding='utf-8') as file:
        content = json.load(file)["subjects"]
        subject_content = None
        for subject in content:
            if subject["subject"] == st.session_state.subject_content:
                subject_content = subject
        if subject_content is not None:
            initial_prompt = prompts.prompt_chatbot
            text = initial_prompt + json_to_text(subject_content)
            st.session_state.text_lesson = text
        else:
            st.error("Error loading subject content to bot")

# Initialize chatbot if not already initialized
if "chatbot" not in st.session_state:
    model = "example_bot"
    st.session_state.chatbot = ChatBot(model, st.session_state.text_lesson)

# Display chat messages from session state
if "messages_chat" not in st.session_state:
    st.session_state.messages_chat = []

ttsModel = TextToVoice()

for message in st.session_state.messages_chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def statistics():
    prompt_statistics = """Analyze all messages provided by the user and return the following statistics: the number of questions asked by the student and the number of correct answers given. Use this format: Questions: X, Correct: Y."""

    st.session_state.chatbot.send_message(prompt_statistics)
    response = st.session_state.chatbot.respond()
    st.write(response)  # Display the statistics on the Streamlit page

# Get user input
if not st.session_state.chat_finished:

    prompt = st.chat_input("Say something")
    ttsModel.play("Say something")
    if prompt:
        if ttsModel.is_playing():
            ttsModel.stop()
        st.session_state.messages_chat.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from chatbot
        with st.chat_message("assistant"):
            stream = st.session_state.chatbot.send_message(prompt)
            response = st.session_state.chatbot.respond()
            st.markdown(response)

        # Append assistant's response to messages_chat
        st.session_state.messages_chat.append({"role": "assistant", "content": response})
        ttsModel.play(text=response)
# Add a button for finishing the chat
if st.button("Finish Chat", disabled=st.session_state.chat_finished):
    statistics()  # Call the statistics function to display final statistics
    st.session_state.chat_finished = True  # Set chat finished status to True
    st.write("Chat finished. You can now review the statistics.")
