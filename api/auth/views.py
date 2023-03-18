from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.students import Student
from ..utils import db, DB_Func
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token
from ..utils.decorators import admin_required


auth_namespace = Namespace('Authentication', description='Operation on authentication')

signup_model = auth_namespace.model(
    "SignUp", {
        "id": fields.Integer(),
        "firstname": fields.String(required=True, description="FIrst name"),
        "lastname": fields.String(required=True, description="Last name"),
        "email": fields.String(required=True, description="An email"),
        "password": fields.String(required=True,description="A password")
    }
)

login_model = auth_namespace.model(
    "Login", {
        "email": fields.String(required=True, description="An email"),
        "password": fields.String(required=True,description="A password")
    }
)

# @auth_namespace.route("/users")
# class GetUsers(Resource):
#     @auth_namespace.marshal_with(user_model)
#     @auth_namespace.doc(
#         description="Retrieve all users"
#     )
#     @admin_required()
#     def get(self):
#         """
#             Retrieve all Users - Admins Only
#         """
#         users = User.query.all()

@auth_namespace.expect(signup_model)
@auth_namespace.marshal_with(signup_model)
class GetUsers(Resource):
    def post(self):
        """
            Signup a student
        """
        data = request.get_json()

        new_student = Student(
            first_name=data.get("firstname"),
            last_name=data.get("lastname"),
            email=data.get("email"),
            password_hash=generate_password_hash(data.get("password")),

        )

        new_student.save_to_db()

        return new_student, HTTPStatus.CREATED

@auth_namespace.route("/login")
class Login(Resource):
    @auth_namespace.expect()
    def post(self):
        """
            Generate JWT Tokens
        """
        data = request.get_json()


        email = data.get("email")
        password = data.get("password")
        user = Student.query.filter_by(email=email)

        if user is not None and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.student_name)
            refresh_token = create_refresh_token(identity=user.student_name)

            response = {
                "access_token":access_token,
                "refresh_token": refresh_token
            }

            return response, HTTPStatus.CREATED
