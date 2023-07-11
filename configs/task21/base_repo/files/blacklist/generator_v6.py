import random
import string

from .blacklist import BlackList

class PasswordGenerator():
    """Class-based password generator"""

    def __init__(self):
        """Constructor for the password generator"""
        self.password_characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        """All characters to be used for the generated passwords"""
        
        self.blacklist = BlackList()
        """Stores a list of password hashes that should not be used"""

    def generate_password(self, password_length = 10):
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