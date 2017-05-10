"""
Utility functions for identity fields on models.
"""

from string import ascii_letters, digits
from random import choice


def generate_model_prefixed_id(model=None, length=32):
    """
    Produces a random model-prefixed string `length` characters long.
    Default of 32 characters (minus prefix) gives ~2.4807E48 possibilities.
    """
    if not model:
        raise ValueError('Model not specified')
    name = model.__class__.__name__.lower()[:4]
    uid = ''.join(choice(ascii_letters + digits) for _ in range(length - 5))
    return '{0}_{1}'.format(name, uid)
