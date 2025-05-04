import messagebird
from ..provider import NotificationProvider
class MessageBirdClient(NotificationProvider):
    def __init__(self, api_key: str, originator: str):
        super().__init__()
        self.name = 'MessageBird'
        self.api_key = api_key
        self.originator = originator
        self.client = messagebird.Client(self.api_key)

    def send_sms(self, to: str, message: str) -> str:
        msg = self.client.message_create(
            self.originator,
            to,
            message
        )
        return msg.id

    def send_call(self, source: str, destination: str) -> str:
        call = self.client.voice_call_create(
            {
                'source': source,
                'destination': destination,
                'callFlow': {
                    'title': 'Simple Flow',
                    'steps': [{
                        'action': 'say',
                        'options': {
                            'payload': 'Hello! This is a test call.',
                            'voice': 'male',
                            'language': 'en-gb'
                        }
                    }]
                }
            }
        )
        return call.id