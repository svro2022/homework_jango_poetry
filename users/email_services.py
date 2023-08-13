from django.core.mail import send_mail

from config import settings


def sendmail(message, recipient, subject='Рассылка Django'):  # отправка письма
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient)
