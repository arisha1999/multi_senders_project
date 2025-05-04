import aiohttp
from ..provider import NotificationProvider
class SMSRuClient(NotificationProvider):
    BASE_URL = "https://sms.ru"

    def __init__(self, api_key: str):
        super().__init__()
        self.name = 'SMS.RU'
        self.api_key = api_key

    async def send_sms(self, to: str, message: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/sms/send", params={
                "api_id": self.api_key,
                "to": to,
                "msg": message,
                "json": 1
            }) as response:
                data = await response.json()
                if data["status"] == "OK":
                    return data["sms"][to]["status_text"]
                else:
                    raise Exception(data["status_text"])

    async def get_balance(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/my/balance", params={
                "api_id": self.api_key,
                "json": 1
            }) as response:
                data = await response.json()
                return data.get("balance", "unknown")

    async def send_bulk_sms(self, numbers: list, message: str) -> dict:
        recipients = ",".join(numbers)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/sms/send", params={
                "api_id": self.api_key,
                "to": recipients,
                "msg": message,
                "json": 1
            }) as response:
                return await response.json()

    async def send_call(self, phone: str, text: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/voice/send", params={
                "api_id": self.api_key,
                "to": phone,
                "msg": text,
                "json": 1
            }) as response:
                data = await response.json()
                if data["status"] == "OK":
                    return data["call_id"]
                else:
                    raise Exception(data["status_text"])
