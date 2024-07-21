import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from connectors.connectors import connection
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, current_user

# Import controllers
from controller.users import user_routes
from controller.accounts import account_routes
from controller.transaction import transaction_routes
from model.users import users

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.register_blueprint(user_routes)
app.register_blueprint(account_routes)
app.register_blueprint(transaction_routes)

login_manager = LoginManager()
login_manager.init_app(app)


# harus di user loader dulu terus di close
@login_manager.user_loader
def load_user(email):
    Session = sessionmaker(connection)
    s = Session()
    user = s.query(users).get(email)
    s.close()
    return user


@app.route("/")
def home():
    return "Welcome to the home page!"


if __name__ == "__main__":
    app.run(debug=True)
