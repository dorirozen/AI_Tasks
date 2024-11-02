from pages.student.chatbot.ChatBotFile import ChatBotFile
from pages.student.chatbot.Terminal import Terminal


class CreateChatBot:

    def __init__(self,chatbot_name,chatbot_text):
        self.chatbot_name = chatbot_name
        self.chatbot_text = chatbot_text

        self.text_plain = ChatBotFile(self.chatbot_name,chatbot_text).plain_text()

        self.terminal = Terminal()

        self.generateChatbot()

    def generateChatbot(self):

        with open(self.chatbot_name, 'w') as file:
            file.write(self.text_plain)

        self.terminal.send(command=f"ollama create {self.chatbot_name} -f ./{self.chatbot_name}")

        print(f"\033[91mCreate chatbot: {self.chatbot_name}\033[0m")