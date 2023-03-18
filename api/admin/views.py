from flask import request
from decouple import config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Namespace, Resource, fields
from ..models.admin import Admin
from ..utils.decorators import admin_required
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity

admin_namespace = Namespace(name="Admin", description="Operations on Admin")


admin_signup_model = admin_namespace.model(
    'AdminSignup', {
        'first_name': fields.String(required=True, description="Admin's First Name"),
        'last_name': fields.String(required=True, description="Admin's Last Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'password': fields.String(required=True, description="Admin's Password")
    }
)

admin_model = admin_namespace.model(
    'Admin', {
        'id': fields.Integer(description="Admin's User ID"),
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'user_type': fields.String(required=True, description="Type of User")
    }
)


admin_signup_model = admin_namespace.model(
    'AdminSignup', {
        'first_name': fields.String(required=True, description="Admin's First Name"),
        'last_name': fields.String(required=True, description="Admin's Last Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'password': fields.String(required=True, description="Admin's Password")
    }
)

admin_model = admin_namespace.model(
    'Admin', {
        'id': fields.Integer(description="Admin's User ID"),
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'user_type': fields.String(required=True, description="Type of User")
    }
)



@admin_namespace.route("/create")
class AdminRegister(Resource):
    @admin_namespace.expect(admin_signup_model)
    @admin_namespace.marshal_with(admin_model)
    def post(self):
        """
        Admin: Register an Admin
        """
        data = request.get_json()
        # instantiate the User class
        new_admin = Admin(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password_hash=generate_password_hash(data.get("password")),
            user_type='admin'

        )

        new_admin.save()

        admin_resp = {}
        admin_resp['id'] = new_admin.id
        admin_resp['first_name'] = new_admin.first_name
        admin_resp['last_name'] = new_admin.last_name
        admin_resp['email'] = new_admin.email
        admin_resp['user_type'] = new_admin.user_type

        return admin_resp, HTTPStatus.CREATED

