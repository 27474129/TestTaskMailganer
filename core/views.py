from __future__ import unicode_literals

import logging
import json
import redis
from .tasks import start_mailing
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MailingSerializer, MailingIdSerializer
from .services import MailingService


logger = logging.getLogger("debug")


class MailingCreation(APIView):
    # method that returns a list of subscribers by mailing_id
    def get(self, request):
        serializer = MailingIdSerializer(data=request.GET)
        if serializer.is_valid():
            r = redis.Redis(host="redis")
            mailing_id = str(json.loads(serializer.data["mailing_id"]))
            return Response({"success": True, "result": r.get(mailing_id)})
        else:
            return Response({"success": False, "message": serializer.errors}, status=400)

    # method that creates a mailing
    def post(self, request, *args, **kwargs):
        # subscribers_format = [["email", "name", "surname"], ["email", "name", "surname"]]
        serializer = MailingSerializer(data=request.POST)
        if serializer.is_valid():
            # due to python version I use default time, below code isnt working
            #  zone = timezone("Europe/Moscow")
            #  start_time = zone.localize(start_time)
            start_time = serializer.data["starttime"]
            mailing_id = MailingService.generate_mailing_id()
            subscribers = serializer.data["subscribers"]
            logger.info("New mailing task registered with id: " + mailing_id)
            start_mailing.apply_async((mailing_id, subscribers), eta=start_time, task_id=mailing_id)
            return Response({"success": True, "mailing_id": mailing_id})
        else:
            return Response({"success": False, "message": serializer.errors}, status=400)
