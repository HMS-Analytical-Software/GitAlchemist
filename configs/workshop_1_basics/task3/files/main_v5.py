# First version of the password generator
# Note that the password in this version is not too safe :-)
import random

# we noticed that random numbers are far too hard to handle
# so we use a fixed seed for now; just for debugging stuff
seed = 42
random.seed(seed)

prefix = "let"
suffix = "mein"

def password_generator_function():
    print("*"*20)
    middle_part = str(random.randint(0,2000))
    print(f"{prefix}{middle_part}{suffix}")
    print("*"*20)

if __name__ == "__main__":
    password_generator_function()