import json
import requests
from pages.student.chatbot.CreateChatBot import CreateChatBot


class ChatBot(CreateChatBot):
    URL = "http://localhost:11434/api/chat"

    def __init__(self, chatbot_name, chatbot_text):
        super().__init__(chatbot_name, chatbot_text)

        self.chatbot_name = chatbot_name.lower()
        self.chatbot_respond = None

        self.message_history = []

    def send_message(self, message) -> None:

        self.message_history.append({"role":"user","content": message})

        params = {"model": self.chatbot_name, "messages": self.message_history}

        response = requests.post(self.URL, json=params, stream=True)

        texts = response.text.split("\n")
        answer = ''

        for j in texts:
            try:
                data = json.loads(j)
            except json.decoder.JSONDecodeError:
                continue

            if not data['done']:
                answer += data['message']['content']

        self.message_history.append({"role": "user", "assistant": message})
        self.chatbot_respond = answer

    def respond(self) -> str:
        return self.chatbot_respond
