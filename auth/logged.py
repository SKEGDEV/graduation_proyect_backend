from flask_bcrypt import check_password_hash, generate_password_hash

class logged:


    def encrypt(self, password_encrypted:str):
        return generate_password_hash(password_encrypted.encode(), 10)

    def match_password(self, password_saved:str, password_encrypted:str):
        return check_password_hash(password_saved.encode(), password_encrypted.encode())






