from rest_framework import serializers


def validate_subscribers(subscribers):
    errors = []
    for subscriber in subscribers:
        if len(subscriber) != 3:
            errors.append("Each subscriber must have 3 fields: email, name, surname")
        if type(subscriber) is not list:
            errors.append("Each subscriber must have List data type")

    raise serializers.ValidationError(errors)


class MailingSerializer(serializers.Serializer):
    starttime = serializers.DateTimeField()
    subscribers = serializers.JSONField(validators=[validate_subscribers])


class MailingIdSerializer(serializers.Serializer):
    mailing_id = serializers.CharField()
