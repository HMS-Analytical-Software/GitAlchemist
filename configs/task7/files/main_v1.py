from generator import PasswordGenerator

if __name__ == "__main__":
    password_generator = PasswordGenerator(use_special = False)
    password_generator.generate_password(20)
    print("Password with digits:")
    password_generator.print_password()

    password_generator = PasswordGenerator(use_digits = False)
    password_generator.generate_password(20)
    print("Password without digits:")
    password_generator.print_password()

    password_generator = PasswordGenerator()
    password_generator.generate_password(20)
    print("Password with special characters and digits:")
    password_generator.print_password()