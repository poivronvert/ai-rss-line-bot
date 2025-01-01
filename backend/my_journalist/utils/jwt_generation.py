import os
import json
import jwt
from dotenv import load_dotenv
from jwt.algorithms import RSAAlgorithm
import time

load_dotenv()

private_key = json.loads(os.getenv("PRIVATE_KEY"))

kid = os.getenv("KID")

headers = {
    "alg": "RS256",
    "typ": "JWT",
    "kid": os.getenv("KID"),
}

payload = {
    "iss": os.getenv("ISS"),
    "sub": os.getenv("SUB"),
    "aud": "https://api.line.me/",
    "exp": int(time.time())+(60 * 30),
    "token_exp": 60 * 60 * 24 * 30
}

key = RSAAlgorithm.from_jwk(private_key)
JWT = jwt.encode(payload, key, algorithm="RS256", headers=headers, json_encoder=None)
