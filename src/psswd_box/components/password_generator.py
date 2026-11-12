from secrets import SystemRandom
from string import ascii_lowercase, ascii_uppercase, digits

LOWERCASE = list(ascii_lowercase)
UPPERCASE = list(ascii_uppercase)
NUMBERS = list(digits)
SYMBOLS = list("!@#$%^&*()-_=+")
POOLS = (LOWERCASE, UPPERCASE, NUMBERS, SYMBOLS)


class PasswordGenerator:
    def __init__(self, rng=None):
        self.rng = rng or SystemRandom()

    def get_pools(self, character_types):
        return [pool for pool, enabled in zip(POOLS, character_types) if enabled]

    def pool_size(self, character_types):
        return sum(len(pool) for pool in self.get_pools(character_types))

    def generate_password(self, character_types, num_characters):
        if num_characters <= 0:
            return ""

        pools = self.get_pools(character_types)
        if not pools:
            return ""

        all_chars = [ch for pool in pools for ch in pool]

        if num_characters < len(pools):
            return "".join(self.rng.choice(all_chars) for _ in range(num_characters))

        chars = [self.rng.choice(pool) for pool in pools]
        chars.extend(
            self.rng.choice(all_chars) for _ in range(num_characters - len(chars))
        )
        self.rng.shuffle(chars)
        return "".join(chars)
