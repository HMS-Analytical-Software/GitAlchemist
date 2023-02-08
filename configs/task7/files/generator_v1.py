import random
import string


class PasswordGenerator():
    """Class-based password generator"""

    def __init__(self, use_digits = True, use_special = True):
        """Constructor for the password generator

        Args:
            use_digits (bool, optional): Boolean to select if digits should be used for password.
            use_special (bool, optional): Boolean to select if special characters should be used for password.
        """
        self.password_characters = list(string.ascii_letters)
        if use_digits:
            self.password_characters.extend(string.digits)
        if use_special:
            self.password_characters.extend("!@#$%^&*()")

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