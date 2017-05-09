"""
Utility functions for identity fields on models.
"""

from string import ascii_letters
from random import choice


def generate_model_uid(model=None, length=42):
    """produces a random model-prefixed string 42 characters long."""
    if not model:
        raise ValueError('Model not specified')
    name = model.__class__.__name__.lower()[:4]
    uid = ''.join(choice(ascii_letters) for _ in range(length - 5))
    return '{0}_{1}'.format(name, uid)
