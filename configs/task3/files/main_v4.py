# First version of the password generator
# Note that the password in this version is not too safe :-)
import random

prefix = "let"
suffix = "mein"

def password_generator_function():
    print("*"*20)
    middle_part = str(random.randint(0,2000))
    print(f"{prefix}{middle_part}{suffix}")
    print("*"*20)

if __name__ == "__main__":
    password_generator_function()