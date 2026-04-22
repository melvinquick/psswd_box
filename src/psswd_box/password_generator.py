from secrets import choice


class PasswordGenerator:
    def __init__(self):
        self.lowercase_letters = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "x",
            "x",
            "y",
            "z",
        ]
        self.uppercase_letters = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        self.numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
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
