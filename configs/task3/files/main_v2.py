# First version of the password generator
# Note that the password in this version is not too safe :-)
import random

def main():
    print("*"*20)
    print("letmein" + str(random.randint(0,2000)))
    print("*"*20)

if __name__ == "__main__":
    main()