from database import mysql
import re
from os import getenv
from auth.logged import logged 

class teacher:

    #validation
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
         
    #Teacher methods
    def create_teacher_user(self, first_name:str, last_name:str, nit:int, password:str, birthday:str, email:str, phone:int):
        try:
            if self.Validate_create_user(first_name, last_name, nit, birthday, email, phone):
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
                if result < 1:
                    return{"msm":"Por algun error de bases de datos su usuario no pudo ser coreado, contactese con servicio al cliente por favor"}
                return {"msm":"Su cuenta ha sido creada con exito, Bienvenido", "token":result}
            return {"msm":"Por motivos de validacion de datos su cuenta no pudo ser creada"}
        except Exception as e:
            return { "msm":"Un error inesperado ha ocurrido", "err":str(e)}

