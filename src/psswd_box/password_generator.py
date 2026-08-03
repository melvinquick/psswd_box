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

    def generate_password(self, character_types=None, num_characters=24):
        if character_types is None:
            character_types = ["y", "y", "y", "y"]

        pools = self.get_pools(character_types)

        if not pools or num_characters <= 0:
            return ""

        password_chars = []

        for pool in pools:
            if len(password_chars) < num_characters:
                password_chars.append(choice(pool))

        all_choices = [char for pool in pools for char in pool]

        while len(password_chars) < num_characters:
            password_chars.append(choice(all_choices))

        self.rng.shuffle(password_chars)

        return "".join(password_chars[:num_characters])

    def get_pools(self, character_types):
        pools = []

        if len(character_types) > 0 and character_types[0] == "y":
            pools.append(self.lowercase_letters)

        if len(character_types) > 1 and character_types[1] == "y":
            pools.append(self.uppercase_letters)

        if len(character_types) > 2 and character_types[2] == "y":
            pools.append(self.numbers)

        if len(character_types) > 3 and character_types[3] == "y":
            pools.append(self.symbols)

        return pools

    def get_valid_choices(self, character_types):
        choices = []

        for pool in self.get_pools(character_types):
            choices.extend(pool)

        return choices
