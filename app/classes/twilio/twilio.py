from twilio.rest import Client

class TwilioClient:
    def __init__(self, account_sid: str, auth_token: str, from_phone: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(self.account_sid, self.auth_token)

    def make_call(self, to: str, twiml_url: str, from_phone: str) -> str:
        call = self.client.calls.create(
            to=to,
            from_=from_phone,
            url=twiml_url
        )
        return call.sid

    def send_sms(self, to: str, message: str, from_phone: str) -> str:
        sent_message = self.client.messages.create(
            body=message,
            from_=from_phone,
            to=to
        )
        return sent_message.sid
