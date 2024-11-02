class ChatBotFile:
    OLLAMA_MODEL = "llama3"
    PLAIN_TEXT_FILE = """FROM {}\n# set the system prompt\nSYSTEM \"\"\"\n{} give me questions about this lesson and after I send you the answet you tell me if is correct or not.\n If the user asks about anything not covered in the lesson, respond with: 'This question is not related to the lesson.'"\n\"\"\""""

    def __init__(self, chatbot_name, prompt):
        self.chatbot_name = chatbot_name
        self.prompt = prompt

    def plain_text(self):
        return self.PLAIN_TEXT_FILE.format(self.OLLAMA_MODEL, self.prompt)
