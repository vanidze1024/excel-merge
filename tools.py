from itertools import chain, product
from string import ascii_uppercase


def column_name_generator():
    for t in chain(
            product(ascii_uppercase, repeat=1),
            product(ascii_uppercase, repeat=2)):
        yield ''.join(t)
