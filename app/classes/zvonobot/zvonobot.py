import requests
import logging
import re
import json
from os import environ
from app.exceptions.call import SendCallRequestFailed
from requests import Session
from app.models.call_template import CallTemplate

class ZvonobotSession(Session):
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = environ.get('F1CALL_ADMIN_PANEL')
        super().__init__()

    def get_balance(self):
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        params = {
            'apiKey': self.api_key,
        }
        try:
            return requests.post(url=self.url + environ.get('F1CALL_BALANCE_PATH'),
                                 data=json.dumps(params),
                                 headers=headers)
        except Exception as ex:
            logging.exception('Failed to get balance via Zvonobot: {e}'.format(e=ex))
            raise SendCallRequestFailed

    def get_call_status(self, related_id_list):
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        data = {
            'apiKey': self.api_key,
            'apiCallIdList': related_id_list
        }
        try:
            return requests.post(url=self.url + environ.get('F1CALL_INFO_PATH'),
                                    data=json.dumps(data),
                                    headers=headers)
        except Exception as ex:
            logging.exception('Failed to get status via Zvonobot: {e}'.format(e=ex))
            raise SendCallRequestFailed

    def send(self, call_template, phones):
        headers = {'accept': 'application/json',
                   'content-type': 'application/json'}
        if call_template.related_id is not None:
            params = {
                'apiKey': self.api_key,
                'phones': phones,
                'templateId': call_template.related_id,
                'outgoingPhone': '',
                'webhookUrl': '{app_url}/api/webhook/zvonobot'.format(app_url=environ.get('APP_URL')),
            }
            try:
                return requests.post(self.url + environ.get('F1CALL_CREATE_WITH_TEMPLATE_PATH'),
                                            data=json.dumps(params),
                                            timeout=15,
                                            headers=headers)
            except Exception as ex:
                logging.exception('Failed to send call via Zvonobot: {e}'.format(e=ex))
                raise SendCallRequestFailed
        else:
            api_key = self.api_key
            json_string = json.dumps(call_template.json)
            json_string = re.sub(r'"name": ".*?", ', "", json_string,
                                 flags=re.UNICODE)  # if in the start of string
            # if in the middle or end of string
            json_string = re.sub(r', "name": ".*?"', "", json_string, flags=re.UNICODE)
            # if it is the only one parameter
            json_string = re.sub(r'"name": ".*?"', "", json_string, flags=re.UNICODE)
            json_string = re.sub(r'"extend": true, ', "", json_string,
                                 flags=re.UNICODE)  # if in the start of string
            # if in the middle or end of string
            json_string = re.sub(r', "extend": true', "",
                                 json_string, flags=re.UNICODE)
            # if it is the only one parameter
            json_string = re.sub(r'"extend": true', "", json_string, flags=re.UNICODE)
            json_string = re.sub(r'"extend": false, ', "", json_string,
                                 flags=re.UNICODE)  # if in the start of string
            # if in the middle or end of string
            json_string = re.sub(r', "extend": false', "",
                                 json_string, flags=re.UNICODE)
            # if it is the only one parameter
            json_string = re.sub(r'"extend": false', "", json_string, flags=re.UNICODE)

            logging.info(json_string)

            params = json.loads(json_string)
            params['apiKey'] = api_key
            params['phones'] = phones
            params['webhookUrl'] = '{app_url}/api/webhook/zvonobot'.format(app_url=environ.get('APP_URL'))
            if call_template.from_duty_phone:
                params['dutyPhone'] = 1
            else:
                params['outgoingPhone'] = str(call_template.outgoing_phone.phone)

            ZvonobotSession.check_tree_element(params, template.source, delivery.id)

            logging.info('Json for calls: ' + json.dumps(params))
            try:
                return requests.post(self.url + environ.get('F1CALL_CREATE_PATH'),
                                            data=json.dumps(params),
                                            timeout=15,
                                            headers=headers)
            except Exception as ex:
                logging.exception('Failed to send call via Zvonobot: {e}'.format(e=ex))
                raise SendCallRequestFailed

    @staticmethod
    def check_tree_element(element, utm_source, delivery_id):
        if element['ivrs']:
            for node in element['ivrs']:
                ZvonobotSession.check_tree_element(node, utm_source, delivery_id)
                if node['webhookParameters']:
                    node['webhookParameters']['utm_source'] = utm_source
                    if delivery_id != 0:
                        node['webhookParameters']['delivery_id'] = str(delivery_id)
                    node['webhookParameters'] = json.dumps(
                        node['webhookParameters'])
                if node['webhookUrl']:
                    node['webhookUrl'] = environ.get(
                        'APP_URL') + node['webhookUrl']

    def get_outgoing_phones(self):
        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        params = {
            'apiKey': self.api_key,
            'all': True
        }
        response = requests.post(self.url + environ.get('F1CALL_GET_OUTGOING_PHONES'),
                                 data=json.dumps(params),
                                 timeout=15,
                                 headers=headers)
        return response

    def delete_record(self, id):
        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        params = {
            'apiKey': self.api_key,
            'idList': [id]
        }
        response = requests.post(url=self.url + environ.get('F1CALL_DELETE_RECORD_PATH'),
                                 data=json.dumps(params),
                                 timeout=15,
                                 headers=headers)
        return response

    def create_record(self, data, files):
        response = requests.post(url=self.url + environ.get('F1CALL_CREATE_RECORD_PATH'),
                                 data=data,
                                 files=files,
                                 timeout=15)
        return response

    def get_records(self):
        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        params = {
            'apiKey': self.api_key,
            'forAmoGet': 1
        }
        response = requests.post(url=self.url + environ.get('F1CALL_GET_RECORDS_PATH'),
                                 data=json.dumps(params),
                                 timeout=15,
                                 headers=headers)
        return response

    def get_templates(self):
        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        params = {
            'apiKey': self.api_key,
            'onlyModerated': 0
        }
        response = requests.post(url=self.url + environ.get('F1CALL_GET_TEMPLATES_PATH'),
                                 data=json.dumps(params),
                                 timeout=15,
                                 headers=headers)
        return response
