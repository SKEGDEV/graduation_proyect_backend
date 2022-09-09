from jwt import decode, encode
from os import getenv
from datetime import datetime, timedelta

class token: 

    def generate_expire_date(self, days: int):
        return (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

    def generate_token(self, token_data:dict):
        return encode(
                payload={**token_data, "expiration":str(self.generate_expire_date(2))}
                ,key=str(getenv("secret_key"))
                ,algorithm="HS256"
                )

    def decrypt_token(self, saved_token:str):
        return decode(saved_token, key=str(getenv("secret_key")), algorithms=["HS256"])

