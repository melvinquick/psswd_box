from secrets import SystemRandom, choice
from string import ascii_lowercase, ascii_uppercase, digits


class PasswordGenerator:
    def __init__(self):
        self.rng = SystemRandom()

        self.lowercase_letters = list(ascii_lowercase)
        self.uppercase_letters = list(ascii_uppercase)
        self.numbers = list(digits)
        self.symbols = [
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "_",
            "=",
            "+",
        ]

    def generate_password(
        self, character_types=["y", "y", "y", "y"], num_characters=20
    ):
        if character_types == ["n", "n", "n", "n"]:
            print("You didn't include any character types... Exiting")
            return exit()

        choices = self.get_valid_choices(character_types)
        character_counter = 0
        psswd = ""

        while character_counter < num_characters:
            psswd += choice(choices)
            character_counter += 1

        return psswd

    def get_valid_choices(self, character_types):
        match character_types:
            case ["y", "y", "y", "y"]:
                return (
                    self.lowercase_letters
                    + self.uppercase_letters
                    + self.numbers
                    + self.symbols
                )
            case ["y", "y", "y", "n"]:
                return self.lowercase_letters + self.uppercase_letters + self.numbers
            case ["y", "y", "n", "n"]:
                return self.lowercase_letters + self.uppercase_letters
            case ["y", "n", "n", "n"]:
                return self.lowercase_letters
            case ["y", "n", "y", "y"]:
                return self.lowercase_letters + self.numbers + self.symbols
            case ["y", "n", "y", "n"]:
                return self.lowercase_letters + self.numbers
            case ["y", "n", "n", "y"]:
                return self.lowercase_letters + self.symbols
            case ["y", "y", "n", "y"]:
                return self.lowercase_letters + self.uppercase_letters + self.symbols
            case ["n", "y", "y", "y"]:
                return self.uppercase_letters + self.numbers + self.symbols
            case ["n", "n", "y", "y"]:
                return self.numbers + self.symbols
            case ["n", "n", "n", "y"]:
                return self.symbols
            case ["n", "y", "n", "y"]:
                return self.uppercase_letters + self.symbols
            case ["n", "y", "n", "n"]:
                return self.uppercase_letters
            case ["n", "n", "y", "n"]:
                return self.numbers
            case ["n", "y", "y", "n"]:
                return self.uppercase_letters + self.numbers
            case ["n", "n", "n", "n"]:
                print("You didn't include any character types... Exiting")
                return exit()
