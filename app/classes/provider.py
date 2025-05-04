class NotificationProvider:
    def __init__(self):
        self.name = 'default'
        self.api_key = ''

    def send_sms(self, **kwargs):
        pass

    def send_call(self, **kwargs):
        pass

    def send_email(self, **kwargs):
        pass

    def get_balance(self, **kwargs):
        pass

    def send_bulk_sms(self, **kwargs):
        pass