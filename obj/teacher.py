from database import mysql
import re
from os import getenv
from auth.logged import logged 
from auth.tokens import token

class teacher:

    #validations
    def Validate_create_user(self, first_name:str, last_name:str, nit:int, birthday:str, email:str, phone:int):
        if re.fullmatch(re.compile(str(getenv('names'))), first_name.upper()) == None: 
            print(re.fullmatch(re.compile(str(getenv('names'))), first_name))
            return False
        if re.fullmatch(re.compile(str(getenv('names'))), last_name.upper()) == None:
            return False
        if nit < 10000000:
            return False
        if re.fullmatch(re.compile(str(getenv('date'))), birthday) == None:
            return False
        if re.fullmatch(re.compile(str(getenv('email'))),email) == None:
            return False
        if phone < 10000000:
            return False
        return True
    
    def User_exists(self, nit:int):
        try:
            connect = mysql.connect()
            cursor = connect.cursor()
            cursor.execute("CALL get_teacher_user_to_validate(%s)",(nit))
            result = cursor.fetchall()
            connect.commit()
            if len(result)>0:
                return False
            return True
        except:
            return False
    #Generate token
    def Generate_token(self, nit:int):
        try:
            connect = mysql.connect()
            cursor = connect.cursor()
            cursor.execute("CALL get_teacher_to_token(%s)",(nit))
            result = cursor.fetchall()
            connect.commit()
            if len(result)>0:
                token_data = {}
                for data in result:
                    token_data = {
                            "id":data[0],
                            "first_name":data[1],
                            "last_name":data[2]
                            }
                    token_return = token().generate_token(token_data)
                    return {"token":token_return}
            return {"msm":"El usuario no existe dentro de la base de datos"} 
        except Exception as e:
            return {"msm":"Ocurrio un error generando el token de sesion ","err": str(e)}
         
    #Teacher methods
    def create_teacher_user(self, first_name:str, last_name:str, nit:int, password:str, birthday:str, email:str, phone:int):
        try:
            if self.Validate_create_user(first_name, last_name, nit, birthday, email, phone):
                if self.User_exists(nit):
                    connect = mysql.connect()
                    cursor = connect.cursor() 
                    result=cursor.execute("CALL Create_teacher(%s, %s, %s, %s, %s, %s, %s)",(
                        first_name.upper(),
                        last_name.upper(),
                        nit,
                        logged().encrypt(password),
                        birthday,
                        email,
                        phone
                        ))
                    connect.commit()  
                    token = self.Generate_token(nit)
                    if result < 1:
                        return{
                        "msm":"Por algun error de bases de datos su usuario no pudo ser coreado, contactese con servicio al cliente por favor"
                        }
                    if not token.get('token'): 
                        return {"msm":"El token no se pudo generar por las razones siguientes", "err":token}
                    return {"msm":"Su cuenta ha sido creada con exito, Bienvenido", "token":token.get('token')}
                return {"msm":"El usuario ya existe dentro de nuestra base de datos por favor ingrese sus datos verdaderos"}
            return {"msm":"Por motivos de validacion de datos su cuenta no pudo ser creada"}
        except Exception as e:
            return { "msm":"Un error inesperado ha ocurrido", "err":str(e)}

    def Get_teacher_user(self, nit:int, password:str):
        try:
            connect = mysql.connect()
            cursor = connect.cursor()
            cursor.execute("CALL get_teacher_user_to_validate(%s)",(nit))
            result = cursor.fetchall()
            connect.commit()
            if len(result)>0:
                password_saved = ""
                for password_search in result:
                   password_saved = password_search[0]
                if logged().match_password(password_saved, password ):
                    token = self.Generate_token(nit)
                    if not token.get('token'):
                        return {"msm":"El token no se pudo generar por las razones siguientes", "err":token}
                    return {"msm":"Bienvenido nuevamente es un gusto poder ayudarlo", "token":token.get('token')}
                return {"msm":"Lo siento pero su contrasena es incorrecta, por favor intente nuevamente"}
            return {"msm": "Lo siento pero este usuario no se ha registrado, por favor registrese para continuar"}
        except Exception as e:
            return {"msm":"Un error insesperado ha ocurrido", "err":str(e)}


