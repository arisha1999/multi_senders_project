import requests
from os import environ
from app.exceptions.sms import SendSmsRequestFailed
from app.classes.logger import logger
from .provider import SmsProvider


class MobizonProvider(SmsProvider):
    def __init__(self, api_key):
        super().__init__()
        self.name = 'Mobizon'
        self.url_pattern = environ.get('MOBIZON_ADMIN_PANEL') + environ.get('MOBIZON_CREATE_PATH')
        self.api_key = api_key

    def send(self, sms):
        try:
            results = []
            error_count = 0
            for item in sms:
                one = self.send_one(item).json()
                one['phone'] = item['phone']
                results.append(one)
                if one['code'] != 0:
                    error_count += 1
            status = 'success' if error_count != len(results) else 'failed'
            result = {'status': status, 'data': results}
            return result
        except Exception as e:
            logger.error('Failed to send many smses via Mobizon: {e}'.format(e=e),
                         extra={"tags": {"service": environ.get('APP_NAME'), "error_type": "regular",
                                         "error_service": "MobizonProvider"}}
                         )
            raise SendSmsRequestFailed

    def send_one(self, sms):
        try:
            headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'cache-control': 'no-cache'
            }
            params = {
                'output': 'json',
                'api': 'v1',
                'apiKey': self.api_key,
                'recipient': sms['phone'],
                'text': sms['text']
            }
            return requests.get(self.url_pattern,
                                params=params,
                                timeout=15,
                                headers=headers)
        except Exception as e:
            logger.error('Failed to send one sms via Mobizon: {e}'.format(e=e),
                         extra={"tags": {"service": environ.get('APP_NAME'), "error_type": "regular",
                                         "error_service": "MobizonProvider"}}
                         )
            raise SendSmsRequestFailed

    def get_balance(self):
        try:
            params = {
                'output': 'json',
                'api': 'v1',
                'apiKey': self.api_key,
            }
            return requests.get(environ.get('MOBIZON_ADMIN_PANEL') + environ.get('MOBIZON_BALANCE_PATH'), params=params)
        except Exception as e:
            logger.error('Failed to send get Mobizon balance: {e}'.format(e=e),
                         extra={"tags": {"service": environ.get('APP_NAME'), "error_type": "regular"},
                                "error_service": "MobizonProvider"}
                         )
            raise SendSmsRequestFailed

    def get_sms_status(self, id):
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'cache-control': 'no-cache'
        }
        params = {
            'output': 'json',
            'api': 'v1',
            'apiKey': self.api_key,
            'criteria[id]': str(id)
        }
        return requests.post(
            url=environ.get('MOBIZON_ADMIN_PANEL') + environ.get('MOBIZON_CAMPAIGN_INFO_PATH'),
            headers=headers,
            data=params,
            timeout=30)


def get_sms_status_by_campaign_id(self, related_id_list):
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'cache-control': 'no-cache'
    }
    params = {
        'output': 'json',
        'api': 'v1',
        'apiKey': self.api_key,
        'criteria[campaignIds]': ','.join([str(id) for id in related_id_list])
    }
    return requests.post(url=environ.get('MOBIZON_ADMIN_PANEL') + environ.get('MOBIZON_CAMPAIGN_INFO_PATH'),
                         headers=headers,
                         data=params,
                         timeout=30)