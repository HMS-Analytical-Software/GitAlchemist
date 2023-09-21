import random
import string
from .config import Config

# TODO: move password characters to config

class PasswordGenerator():
    """Class-based password generator"""

    def __init__(self):
        """Constructor for the password generator"""
        cfg = Config()
        self.password_characters = list(cfg.CHARS_DEFAULT + cfg.CHARS_SPECIAL)

    def generate_password(self, password_length=Config.DEFAULT_PASSWORD_LENGTH):
        """The function that generates the password"""
        self.password = ""
        for i in range(password_length):
            random_number = random.randint(0, len(self.password_characters) - 1)
            self.password += self.password_characters[random_number]

    def print_password(self):
        """The function that shows the password in the terminal"""
        print("*" * 20)
        print(f"{self.password}")
        print("*"*20)
