from twilio.rest import Client

class TwilioClient:
    def __init__(self, account_sid: str, auth_token: str, from_phone: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(self.account_sid, self.auth_token)

    # ✅ Sending call
    def make_call(self, to: str, twiml_url: str, from_phone: str) -> str:
        call = self.client.calls.create(
            to=to,
            from_=from_phone,
            url=twiml_url
        )
        return call.sid

    # ✅ Sending sms
    def send_sms(self, to: str, message: str, from_phone: str) -> str:
        sent_message = self.client.messages.create(
            body=message,
            from_=from_phone,
            to=to
        )
        return sent_message.sid
    
    # ✅ Phone number management
    def search_available_numbers(self, country: str = "US", area_code: str = None, limit: int = 5):
        return self.client.available_phone_numbers(country).local.list(area_code=area_code, limit=limit)

    def buy_number(self, phone_number: str):
        return self.client.incoming_phone_numbers.create(phone_number=phone_number)

    # ✅ Monitoring
    def list_calls(self, limit: int = 5):
        return self.client.calls.list(limit=limit)

    def list_sms_messages(self, limit: int = 5):
        return self.client.messages.list(limit=limit)

    def get_usage_summary(self, limit: int = 5):
        return self.client.usage.records.today.list(limit=limit)[0]