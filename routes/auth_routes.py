from flask import Blueprint, request, jsonify
from obj.teacher import teacher

auth = Blueprint('auth', __name__)

@auth.route("/auth/signup", methods=["POST"])
def auth_signup():
    set_data = request.get_json() 
    result = teacher().create_teacher_user(
            set_data["first_name"], 
            set_data["last_name"],
            set_data["nit"],
            set_data["password"],
            set_data["birthday"],
            set_data["email"],
            set_data["phone"] 
            )
    if not result.get('token'):
        response = jsonify(result)
        response.status_code = 403 
        return response
    response = jsonify(result)
    response.status_code =200
    return response
    

