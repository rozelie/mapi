from twilio.rest import Client

from mapi.config import settings


def send_message(body: str) -> None:
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    client.messages.create(
        to=settings.twilio_my_phone_number,
        from_=settings.twilio_virtual_phone_number,
        body=body,
    )
