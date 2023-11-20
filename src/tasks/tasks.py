from pathlib import Path

from src.tasks._celery import celery
from PIL import Image


@celery.task
def process_pic(path: str):
    path = Path(path)
    im = Image.open(path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_1000_500.save(f'src/static/images/1000_500_{path.name}')

    im_resized_200_100 = im.resize((200, 100))
    im_resized_200_100.save(f'src/static/images/200_100_{path.name}')
