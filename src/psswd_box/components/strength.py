import math

WEAK_BELOW = 45.0
STRONG_AT = 80.0
TARGET_BITS = 128.0


def entropy_bits(pool_size, length):
    if pool_size <= 1 or length <= 0:
        return 0.0
    return length * math.log2(pool_size)


def classify(bits):
    if bits < WEAK_BELOW:
        return "weak"
    if bits < STRONG_AT:
        return "fair"
    return "strong"


def percent(bits):
    return max(0, min(100, int(bits / TARGET_BITS * 100)))
