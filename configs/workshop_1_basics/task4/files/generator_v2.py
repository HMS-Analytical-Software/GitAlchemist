import random


class PasswordGenerator():
    """Class-based password generator"""

    def __init__(self, seed=42):
        self.prefix = "let"
        self.suffix = "mein"

        # initialize the generator with a static seed
        random.seed(seed)

    def password_generator_function(self):
        print("*"*20)
        middle_part = str(random.randint(0,2000))
        print(f"{self.prefix}{middle_part}{self.suffix}")
        print("*"*20)