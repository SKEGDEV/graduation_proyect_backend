from flask import jsonify, request
from functools import wraps
#need to validate using mysql:
#-stored session token
#-Session token expiration
from database import mysql
from tokens import token

class token_validation:

    def verify_token(self):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or 'Bearer' not in auth_header:
                return {"msm":"Perdon usted no cuenta con un token de session por favor inicie sesion para continuar"}
            if not len(auth_header.split(' ')) == 2:
                return {"msm": "Perdon su token de session es invalido por favor inicie sesion de nuevo para continuar"}
            token().saved_token = auth_header.split(' ')[1]
            return {"usr": token().decrypt_token()}
        except Exception as e:
           return {
                    "msm":"Un error inesperado ha ocurrido",
                    "err":str(e) 
                    }

    def token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            res = self.verify_token()
            if not res.get('usr') and not res.get('err'):
                response = jsonify({
                    "msm": res.get('msm') 
                    })
                response.status_code = 403 
                return response
            if not res.get('usr'):
                response = jsonify({
                    "msm": res.get('msm'),
                    "err": res.get('err')
                    })
                response.status_code = 403
                return response
            return f(*args, **kwargs)
        return decorated

            



