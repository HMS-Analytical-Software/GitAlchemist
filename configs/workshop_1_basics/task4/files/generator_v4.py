import random
import string


class PasswordGenerator():
    """Class-based password generator"""

    def __init__(self, seed=42):
        """Constructor for the password generator

        Args:
            seed (int, optional): Seed for the pseudo random number generator. Defaults to 42.
        """
        self.password_characters = list(string.ascii_letters + string.digits)

        # initialize the generator with a static seed
        random.seed(seed)

    def password_generator_function(self):
        """The function that shows the password in the terminal"""
        password = ""
        for i in range(10):
            random_number = random.randint(0, len(self.password_characters) - 1)
            password += self.password_characters[random_number]

        print("*" * 20)
        print(f"{password}")
        print("*"*20)