from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


auth_bp = Blueprint(
    "auth_bp",
    __name__,
    url_prefix="/api/auth"
)

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "error": "Username, email and password are required"
        }), 400

    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        return jsonify({
            "error": "Username already exists"
        }), 409

    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return jsonify({
            "error": "Email already exists"
        }), 409

    password_hash = generate_password_hash(password) #here we use password_hash so that the password is encrypted and not stored in plain text.The user can login with the password but the password will not be stored in plain text.

    new_user = User( #the password will be stored as like 'mypassword123' but the pass_hash will store the hash of the password which is like 'asjgdjgsdfhgsdfghsmjdfhg' so here whenever the user login it will match the hash not the password
        username=username, #type: ignore
        email=email, #type: ignore
        password_hash=password_hash #type: ignore
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    user = User.query.filter_by(
        username=username  #this to find the user if already created 
    ).first()

    if user is None:
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    if not check_password_hash(
        user.password_hash,
        password  #it checks if the entered password is in the pass hash or not
    ):
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    access_token = create_access_token(
        identity=str(user.id)  #this for creation of JWT
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    })

