import random

# we noticed that random numbers are far too hard to handle
# so we use a fixed seed for now; just for debugging stuff
seed = 42
random.seed(seed)


class PasswordGenerator():
    """Class-based password generator"""

    def __init__(self):
        self.prefix = "let"
        self.suffix = "mein"

    def password_generator_function(self):
        print("*"*20)
        middle_part = str(random.randint(0,2000))
        print(f"{self.prefix}{middle_part}{self.suffix}")
        print("*"*20)