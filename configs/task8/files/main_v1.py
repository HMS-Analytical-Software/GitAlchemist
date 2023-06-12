import argparse
from pathlib import Path
from generator import PasswordGenerator

def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--special_characters",
                       action='store_true',
                       default=False,
                       help="Flag for usage of special characters in generated password (default: False)")
    parser.add_argument("--digits",
                       action='store_true',
                       default=False,
                       help="Flag for usage of digits in generated password (default: False)")
    parser.add_argument("-l", "--length",
                        action='store',
                        default='12',
                        type=int,
                        help="Password length (default: 12)")

    return parser

if __name__ == "__main__":
    parser = setup_argparse()
    args = parser.parse_args()

    password_generator = PasswordGenerator(use_digits = args.digits, use_special = args.special_characters)
    password_generator.generate_password(args.length)
    password_generator.print_password()