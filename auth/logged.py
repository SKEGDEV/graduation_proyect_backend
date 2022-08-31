from flask_bcrypt import check_password_hash, generate_password_hash

class logged:

    def __init__(self):
        self.password_saved = ""
        self.password_encrypted = ""

    @property
    def password_saved(self):
        return self.password_saved

    @password_saved.setter
    def password_saved(self, value:str):
        self.password_saved = value

    @property
    def password_encrypted(self):
        return self.password_encrypted

    @password_encrypted.setter
    def password_encrypted(self, value:str):
        self.password_encrypted = value

    def encrypt(self):
        return generate_password_hash(self.password_encrypted.encode(), 10)

    def match_password(self):
        return check_password_hash(self.password_saved.encode(), self.password_encrypted.encode())






