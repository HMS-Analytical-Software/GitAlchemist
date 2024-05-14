from generator import PasswordGenerator

if __name__ == "__main__":
    password_generator = PasswordGenerator()
    password_generator.generate_password()
    password_generator.print_password()