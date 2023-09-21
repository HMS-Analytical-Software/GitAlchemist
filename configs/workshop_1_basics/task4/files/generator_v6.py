import random


class PasswordGenerator():
    """Class-based password generator"""

    def __init__(self, seed=43):
        """Constructor for the password generator

        Args:
            seed (int, optional): Seed for the pseudo random number generator. Defaults to 43.
        """
        self.prefix = "let"
        self.suffix = "mein"

        # initialize the generator with a static seed
        random.seed(seed)

    def password_generator_function(self):
        """The function that shows the password in the terminal"""
        print("*"*20)
        middle_part = str(random.randint(0,2000))
        print(f"{self.prefix}{middle_part}{self.suffix}")
        print("*"*20)