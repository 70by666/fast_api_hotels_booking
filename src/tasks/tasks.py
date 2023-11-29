import smtplib
from pathlib import Path

from pydantic import EmailStr

from src.config import settings
from src.tasks._celery import celery
from PIL import Image

from src.tasks._email import create_booking_message


@celery.task
def process_pic(path: str):
    path = Path(path)
    im = Image.open(path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_1000_500.save(f'src/static/images/1000_500_{path.name}')

    im_resized_200_100 = im.resize((200, 100))
    im_resized_200_100.save(f'src/static/images/200_100_{path.name}')


@celery.task
def send_booking_email(booking: dict, email_to: EmailStr):
    msg_content = create_booking_message(booking, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
