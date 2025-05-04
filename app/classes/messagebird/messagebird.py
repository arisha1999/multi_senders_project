import messagebird

class MessageBirdClient:
    def __init__(self, api_key: str, originator: str):
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

    def make_call(self, source: str, destination: str) -> str:
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