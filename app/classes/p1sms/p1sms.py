import json
from os import environ
import socket
import requests
from unittest.mock import patch
from app.exceptions.sms import SendSmsRequestFailed
from .provider import SmsProvider
from app.classes.logger import logger

getaddrinfo = socket.getaddrinfo

def getaddrinfoIPv4(host, port, family=0, type=0, proto=0, flags=0):
    """
    Monkey patch for force use IPv4 protocol on requests library
    """
    return getaddrinfo(host=host, port=port, family=socket.AF_INET, type=type, proto=proto, flags=flags)

class P1smsProvider(SmsProvider):
    def __init__(self, api_key):
        super().__init__()
        self.name = 'P1sms'
        self.url_pattern = environ.get('P1SMS_ADMIN_PANEL') + environ.get('P1SMS_CREATE_PATH')
        self.api_key = api_key

    def send(self, sms):
        try:
            headers = {'accept': 'application/json',
                    'content-type': 'application/json'}
            params = {
                'apiKey': self.api_key,
                'webhookUrl': '{app_url}/api/webhook/p1sms'.format(app_url=environ.get('APP_URL')),
                'sms': sms
            }

            with patch('socket.getaddrinfo', side_effect=getaddrinfoIPv4):
                return requests.post(self.url_pattern,
                                     data=json.dumps(params),
                                     timeout=15,
                                     headers=headers)
        except Exception as e:
            logger.error('Failed to send sms via P1sms: {e}'.format(e=e),
                extra={"tags": {"service": environ.get('APP_NAME'), "error_type": "regular", "error_service": "P1smsProvider"}}
            )
            raise SendSmsRequestFailed

    def get_balance(self):
        try:
            headers = {
                'accept': 'application/json',
                'content-type': 'application/json'
            }
            params = {
                'apiKey': self.api_key,
            }
            return requests.get(url=environ.get('P1SMS_ADMIN_PANEL') + environ.get('P1SMS_BALANCE_PATH'),
                                data=json.dumps(params),
                                headers=headers)
        except Exception as e:
            logger.error('Failed to get balance sms via P1sms: {e}'.format(e=e),
                extra={"tags": {"service": environ.get('APP_NAME'), "error_type": "regular", "error_service": "P1smsProvider"}}
            )
            raise SendSmsRequestFailed

    def get_balance_credit(self):
        try:
            headers = {
                'accept': 'application/json',
                'content-type': 'application/json'
            }
            params = {
                'apiKey': self.api_key,
            }
            return requests.get(url=environ.get('P1SMS_ADMIN_PANEL') + environ.get('P1SMS_BALANCE_CREDIT_PATH'),
                                data=json.dumps(params),
                                headers=headers)
        except Exception as e:
            logger.error('Failed to get credit balance sms via P1sms: {e}'.format(e=e),
                extra={"tags": {"service": environ.get('APP_NAME'), "error_type": "regular", "error_service": "P1smsProvider"}}
            )
            raise SendSmsRequestFailed

    def get_sms_status(self, related_id_list):
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        data = {
            'apiKey': self.api_key,
            'apiSmsIdList': related_id_list
        }
        return requests.post(url=environ.get('P1SMS_ADMIN_PANEL') + environ.get('P1SMS_INFO_PATH'),
                                               headers=headers,
                                               data=json.dumps(data),
                                               timeout=30)