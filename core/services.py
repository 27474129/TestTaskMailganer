import redis
import logging
from random import randint
from django.core.mail import send_mail
from mailganer.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from django.template import loader
from celery.utils.log import get_task_logger


# celery logger
logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


class MailingService:
    @staticmethod
    def generate_mailing_id():
        r = redis.Redis(host="redis")
        while True:
            mailing_id = str(randint(1, 999999))
            if r.get(mailing_id) is None:
                logger.info("Created mailing id: " + mailing_id)
                return mailing_id

    @staticmethod
    def send(user_email, name, surname):
        html_document = loader.render_to_string('core/mailing_message.html', {
            "name": name,
            "surname": surname
        })
        send_mail(
            "Mailing",
            "Mailing",
            EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
            auth_user=EMAIL_HOST_USER,
            auth_password=EMAIL_HOST_PASSWORD,
            html_message=html_document
        )
        logger.info("Sended to: " + user_email)
