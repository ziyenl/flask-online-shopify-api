from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256
from db import db
from models import UserModel
from schema import UserSchema


blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegistration(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        Register new user to the system
        :param user_data: user data consisting of name and password
        :return: str
        """
        if UserModel.query.filter(UserModel.name == user_data['name']).first():
            abort(409, "Username already exist.")
        user = UserModel(name=user_data['name'],
                        password=pbkdf2_sha256.hash(user_data['password'])) # hash the password
        db.session.add(user)
        db.session.commit()

        return {"message": "User successfully created."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        :return:
        """
        user = UserModel.query.filter(UserModel.name == user_data['name']).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(user.id)
            return {"access_token" : access_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    Get a  User, Deleting User for testing purposes.
    """
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """
        Get a user
        :param user_id: user id
        :return: user
        """
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        """
        Delete a user
        :param user_id: user id
        :return: str
        """
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200