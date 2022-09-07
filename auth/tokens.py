from jwt import decode, encode
from os import getenv
from datetime import datetime, timedelta

class token:
    def __init__(self,):
        self.saved_token = ""
        self.token_data = {}

    @property
    def saved_token(self):
        return self.token

    @saved_token.setter
    def saved_token(self, value:str):
        self.token = value

    @property
    def token_data(self):
        return self.data

    @token_data.setter
    def token_data(self, value:dict):
        self.data = value

    def generate_expire_date(self, days: int):
        return (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

    def generate_token(self):
        return encode(
                payload={**self.token_data, "expiration":str(self.generate_expire_date(2))}
                ,key=str(getenv("secret_key"))
                ,algorithm="HS256"
                )

    def decrypt_token(self):
        return decode(self.saved_token, key=str(getenv("secret_key")), algorithms=["HS256"])

