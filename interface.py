import os
from typing import List

class ChatInterface:
    def __init__(self):
        self.width = 80
        self.padding = 2

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_header(self):
        print('=' * self.width)
        print('IIIT Nagpur Chatbot'.center(self.width))
        print('=' * self.width)

    def show_welcome(self):
        welcome_message = [
            "Welcome to the IIIT Nagpur Chatbot!",
            "I'm here to help you learn about our institute.",
            "You can ask me about:",
            "- Academic programs and courses",
            "- Campus facilities",
            "- Admission procedures",
            "- Student life",
            "- And more!"
        ]
        print('\n')
        for line in welcome_message:
            print((' ' * self.padding) + line)
        print('\n')

    def show_footer(self):
        print('-' * self.width)
        print('Type "help" for commands or "exit" to quit'.center(self.width))
        print('-' * self.width)

    def show_help(self):
        help_commands = [
            ("help", "Show this help message"),
            ("clear", "Clear the conversation history"),
            ("exit", "Exit the chatbot"),
        ]
        print('\nAvailable commands:')
        for cmd, desc in help_commands:
            print(f"{' ' * self.padding}{cmd:10} - {desc}")
        print('\n')

    def format_message(self, message: str, sender: str) -> str:
        prefix = "You: " if sender == "user" else "Bot: "
        return f"{prefix}{message}"

    def show_message(self, message: str, sender: str):
        formatted = self.format_message(message, sender)
        print(formatted)

    def show_error(self, message: str):
        print(f"\nError: {message}\n") 