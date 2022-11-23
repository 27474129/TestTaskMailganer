import redis
import json
from mailganer.celery_ import app
from .services import MailingService


@app.task
def start_mailing(mailing_id, subscribers):
    r = redis.Redis(host="redis")
    r.set(mailing_id, json.dumps({"subscribers": subscribers}))
    # I decided to simplify the json data to make it easier for you to check
    for subscriber in subscribers:
        MailingService.send(
            user_email=subscriber[0],
            name=subscriber[1],
            surname=subscriber[2]
        )
