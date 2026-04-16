import requests
import time
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

BASE_URL = "https://testnet.binancefuture.com"


def sign(params):
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(
        API_SECRET.encode(),
        query_string.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature


def place_market_order(symbol, side, quantity):
    endpoint = "/fapi/v1/order"

    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": int(time.time() * 1000)
    }

    params["signature"] = sign(params)

    headers = {
        "X-MBX-APIKEY": API_KEY
    }

    response = requests.post(BASE_URL + endpoint, params=params, headers=headers)

    return response.json()

def place_limit_order(symbol, side, quantity, price):
    endpoint = "/fapi/v1/order"

    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": "GTC",
        "timestamp": int(time.time() * 1000)
    }

    params["signature"] = sign(params)

    headers = {
        "X-MBX-APIKEY": API_KEY
    }

    response = requests.post(BASE_URL + endpoint, params=params, headers=headers)

    return response.json()