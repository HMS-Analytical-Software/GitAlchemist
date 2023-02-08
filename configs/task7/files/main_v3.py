from generator import PasswordGenerator

if __name__ == "__main__":
    password_generator = PasswordGenerator(use_special = False)
    password_generator.generate_password(20)
    password_generator.print_meta()
    password_generator.print_password()
    print("")
    password_generator = PasswordGenerator(use_digits = False)
    password_generator.generate_password(20)
    password_generator.print_meta()
    password_generator.print_password()
    print("")
    password_generator = PasswordGenerator()
    password_generator.generate_password(20)
    password_generator.print_meta()
    password_generator.print_password()