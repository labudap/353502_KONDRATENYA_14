"""Common UI components"""
from typing import Callable, Dict

class Menu:
    def __init__(self, title: str, options: Dict[str, str]):
        self.title = title
        self.options = options

    def display(self):
        print(f"\n{'='*40}")
        print(f"{self.title.center(40)}")
        print(f"{'='*40}")
        for key, desc in self.options.items():
            print(f"{key}. {desc}")

    def get_choice(self, prompt: str = "Enter your choice: ") -> str:
        while True:
            choice = input(prompt).strip().upper()
            if choice in self.options:
                return choice
            print("Invalid choice. Please try again.")

def get_valid_input(prompt: str, validator: Callable, error_msg: str = "Invalid input") -> str:
    while True:
        user_input = input(prompt).strip()
        if validator(user_input):
            return user_input
        print(error_msg)