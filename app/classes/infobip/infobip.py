import httpx

class InfobipClient:
    def __init__(self, api_key: str, base_url: str, sms_sender: str, email_from: str, email_from_name: str):
        self.api_key = api_key
        self.base_url = base_url
        self.sms_sender = sms_sender
        self.email_from = email_from
        self.email_from_name = email_from_name
        self.headers = {
            "Authorization": f"App {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def send_sms(self, to: str, text: str) -> str:
        url = f"{self.base_url}/sms/2/text/advanced"
        payload = {
            "messages": [{
                "from": self.sms_sender,
                "destinations": [{"to": to}],
                "text": text
            }]
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()["messages"][0]["messageId"]

    async def make_call(self, to: str, audio_url: str) -> str:
        url = f"{self.base_url}/voice/1/calls"
        payload = {
            "from": self.sms_sender,
            "to": to,
            "destination": {
                "type": "number",
                "number": to
            },
            "record": False,
            "anonymous": False,
            "callRouting": {
                "callOption": {
                    "type": "audioFile",
                    "audioFileUrl": audio_url
                }
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json().get("callId", "Call initiated")

    async def send_email(self, to: str, subject: str, body: str) -> str:
        url = f"{self.base_url}/email/2/send"
        payload = {
            "from": {
                "emailAddress": self.email_from,
                "name": self.email_from_name
            },
            "to": [{"emailAddress": to}],
            "subject": subject,
            "html": f"<p>{body}</p>"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json().get("messageId", "Email sent")
