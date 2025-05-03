import vonage

class NexmoClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def send_sms(self, to: str, message: str, from_name: str) -> str:
        client = vonage.Client(key=self.api_key, secret=self.api_secret)
        sms = vonage.Sms(client)
        response = sms.send_message({
            "from": from_name,
            "to": to,
            "text": message,
        })

        if response["messages"][0]["status"] != "0":
            raise Exception(f"SMS failed: {response['messages'][0]['error-text']}")

        return response["messages"][0]["message-id"]

    def make_call(self, to: str, answer_url: str, from_number: str) -> str:
        client = vonage.Client(key=self.api_key, secret=self.api_secret)
        voice = vonage.Voice(client)
        response = voice.create_call({
            "to": [{"type": "phone", "number": to}],
            "from": {"type": "phone", "number": from_number},
            "answer_url": [answer_url]
        })
        return response.get("uuid")