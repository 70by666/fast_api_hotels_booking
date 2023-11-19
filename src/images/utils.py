import os
from uuid import uuid4


def set_name(name):
    files = os.listdir('src/static/images')
    for i in files:
        if i.replace('.webp', '') == str(name):
            name = f'{name}_{uuid4().hex[:8]}'
    return str(name)
