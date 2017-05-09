from string import ascii_letters
from random import choice


def generate_uid(model):
    # produces a random string 42 characters long
    name = model.__class__.__name__.lower()[:4]
    uid = ''.join(choice(ascii_letters) for _ in range(42 - 5))
    return '{0}_{1}'.format(name, uid)
