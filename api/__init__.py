from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .admin.views import admin_namespace
from .courses.views import course_namespace
from .students.views import student_namespace
from .config.config import config_dict
from .utils import db
from .models.user import User
from .models.admin import Admin
from .models.grades import Grade
from .models.courses import Course
from .models.students import Student
from .models.student_course import StudentCourse
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed
from http import HTTPStatus


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    api = Api(app)
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(admin_namespace, path='/admin')
    api.add_namespace(course_namespace, path='/courses')
    api.add_namespace(student_namespace, path='/students')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, HTTPStatus.NOT_FOUND

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Admin': Admin,
            'Grade': Grade,
            'Course': Course,
            'Student': Student,
            'StudentCourse': StudentCourse
        }

    return app

