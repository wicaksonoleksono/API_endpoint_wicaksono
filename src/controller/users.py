from flask import Blueprint, request, jsonify

from connectors.connectors import connection
from sqlalchemy.orm import sessionmaker

from model.users import users

from flask_login import login_user, logout_user, login_required, current_user

user_routes = Blueprint("user_routes", __name__)


# register User
@user_routes.route("/register", methods=["POST"])
def register_user():
    Session = sessionmaker(bind=connection)
    s = Session()
    s.begin()
    try:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            return jsonify({"message": "Missing required fields"}), 400

        new_user = users(username=username, email=email)
        new_user.set_password(password)
        s.add(new_user)
        s.commit()
        return jsonify({"message": "User created"}), 200
    except Exception as e:
        s.rollback()
        return jsonify({"message": "error registering", "error": str(e)}), 500
    finally:
        s.close()


#  Login
@user_routes.route("/login", methods=["POST"])
def check_login():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        email = request.form["email"]
        password = request.form["password"]
        user = s.query(users).filter(users.email == email).first()
        if user is None:
            print("User not found")
            return jsonify({"message": "User not found"}), 403
        if not user.check_password(password):
            print("Invalid password")
            return jsonify({"message": "Invalid password"}), 403

        login_user(user)
        session_id = request.cookies.get("session")
        return jsonify({"session_id": session_id, "message": "Login successful!"}), 200

    except Exception as e:
        s.rollback()
        return jsonify({"message": "Failed to login", "error": str(e)}), 500
    finally:
        s.close()


#  Logout


@user_routes.route("/logout", methods=["GET"])
@login_required
def user_logout():
    logout_user()
    return {"message": "Success logout"}


@user_routes.route("/profile", methods=["GET"])
@login_required
def get_profile():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        profile_data = {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "created_at": current_user.created_at,
            "updated_at": current_user.updated_at,
        }
        return jsonify(profile_data), 200

    except Exception as e:
        s.rollback()
        return jsonify({"message": "Failed to fetch profile", "error": str(e)}), 500
    finally:
        s.close()


#  edit profile


@user_routes.route("/profile", methods=["PUT"])
def update_profile():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        user = s.query(users).get(current_user.id)
        user.username = request.form["username"]
        user.email = request.form["email"]
        user.set_password(request.form["password"])
        s.commit()
        return {"message": "Profile updated"}, 200
    except Exception as e:
        return {"message": "something went wrong", "error": str(e)}, 500
    finally:
        s.close()
