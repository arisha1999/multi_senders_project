import requests
import json
from os import environ
from app.exceptions.sms import SendSmsRequestFailed
from app.classes.logger import logger
from .provider import SmsProvider


class UnicoreProvider(SmsProvider):
    def __init__(self):
        super().__init__()
        self.name = 'Unicore'
        self.url_pattern = environ.get('UNICODE_ADMIN_PANEL')

    def send(self, params):
        try:
            results = []
            error_count = 0
            for item in params:
                one = self.send_one(item).json()
                results.append(one)
                if one.get('status', None) == 'error' or one.get('error', None):
                    error_count += 1
            status = 'success' if error_count != len(results) else 'failed'
            result = {'status': status, 'data': results}
            return result
        except Exception as e:
            logger.error('Failed to send many smses via Unicore: {e}'.format(e=e),
                         extra={"tags": {"service": environ.get('APP_NAME'), "error_type": "regular",
                                         "error_service": "UnicoreProvider"}}
                         )
            raise SendSmsRequestFailed

    def send_one(self, params):
        try:
            return requests.post(self.url_pattern,
                                data=params,
                                timeout=15)
        except Exception as e:
            logger.error('Failed to send one sms via Unicore: {e}'.format(e=e),
                         extra={"tags": {"service": environ.get('APP_NAME'), "error_type": "regular",
                                         "error_service": "UnicoreProvider"}}
                         )
            raise SendSmsRequestFailed
