from django.conf.urls import url
from .views import MailingCreation


urlpatterns = [
    url("", MailingCreation.as_view(), name="base_api_url"),
]
