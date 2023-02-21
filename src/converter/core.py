from aiohttp import ClientSession
from cache import AsyncTTL

API_KEY = "494SjLSFgq9t3VSZaxN2zituy0EseWj5vQ2v4Lyn"
CURRENCY_API_BASE_URL = "https://api.currencyapi.com/v3/latest"


class RemoteException(Exception):
    def __init__(self, status, errors):
        self.status = status
        self.errors = errors


@AsyncTTL(time_to_live=60)
async def get_rate(from_currency: str, to_currency: str) -> float:
    params = {
        "apikey": API_KEY,
        "currencies": to_currency,
        "base_currency": from_currency,
    }
    async with ClientSession() as session:
        async with session.get(CURRENCY_API_BASE_URL, params=params) as resp:
            json = await resp.json()
            if resp.status != 200:
                raise RemoteException(status=resp.status, errors=json["errors"])
            return json["data"][to_currency]["value"]
