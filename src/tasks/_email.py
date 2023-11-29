from email.message import EmailMessage
from pydantic import EmailStr

from src.config import settings


def create_booking_message(booking: dict, email_to: EmailStr):
    email = EmailMessage()
    email['Subject'] = 'Подтверждение бронирования'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to
    email.set_content(
        f'''
            <h1> Бронирование номера </h1>
            {booking}
        ''',
        subtype='html',
    )

    return email
