from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
from connectors.connectors import connection
from model.accounts import accounts

account_routes = Blueprint("account_routes", __name__)


@account_routes.route("/accounts", methods=["POST"])
@login_required
def create_account():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        account_type = request.form["account_type"]
        if account_type not in ["checking", "deposit", "savings"]:
            return (
                jsonify(
                    {
                        "message": "Invalid account type either checking deposit or savings"
                    }
                ),
                400,
            )

        balance = request.form["balance"]

        if not balance:
            return jsonify({"message": "Missing balance"}), 400

        new_account = accounts(
            user_id=current_user.id,
            account_type=account_type,
            balance=balance,
        )

        s.add(new_account)
        s.commit()
        return (
            jsonify(
                {
                    "message": "Account created successfully",
                    "account_number": new_account.account_number,
                }
            ),
            201,
        )
    except Exception as e:
        s.rollback()
        return jsonify({"message": "Error creating account", "error": str(e)}), 500
    finally:
        s.close()


@account_routes.route("/accounts", methods=["GET"])
@login_required
def get_accounts():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        user_accounts = s.query(accounts).filter_by(user_id=current_user.id).all()
        accounts_list = [
            {
                "id": user_account.id,
                "account_type": user_account.account_type,
                "account_number": user_account.account_number,
                "balance": float(user_account.balance),
                "created_at": user_account.created_at,
                "updated_at": user_account.updated_at,
            }
            for user_account in user_accounts
        ]
        return jsonify(accounts_list), 200
    except Exception as e:
        s.rollback()
        return jsonify({"message": "Error fetching accounts", "error": str(e)}), 500
    finally:
        s.close()


@account_routes.route("/accounts/<id>", methods=["GET"])
@login_required
def get_account_by_id(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        account = s.query(accounts).filter_by(id=id, user_id=current_user.id).first()
        if not account:
            return {"message": "Account not found"}, 404
        account_details = {
            "id": account.id,
            "account_type": account.account_type,
            "account_number": account.account_number,
            "balance": float(account.balance),
            "created_at": account.created_at,
            "updated_at": account.updated_at,
        }
        return jsonify(account_details), 200
    except Exception as e:
        return {"message": "Error fetching account", "error": str(e)}, 500
    finally:
        s.close()


@account_routes.route("/accounts/<id>", methods=["PUT"])
@login_required
def edit_account(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        account = s.query(accounts).filter_by(id=id, user_id=current_user.id).first()
        if not account:
            return {"message": "Account not found"}, 404

        account.account_type = request.form.get("account_type", account.account_type)

        s.commit()
        return {"message": "Account updated successfully"}, 200
    except Exception as e:
        s.rollback()
        return {"message": "Error updating account", "error": str(e)}, 500
    finally:
        s.close()


@account_routes.route("/accounts/<id>", methods=["DELETE"])
@login_required
def delete_account(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        account = s.query(accounts).filter_by(id=id, user_id=current_user.id).first()
        if not account:
            return {"message": "Account not found"}, 404

        s.delete(account)
        s.commit()
        return {"message": "Account deleted successfully"}, 200
    except Exception as e:
        s.rollback()
        return {"message": "Error deleting account", "error": str(e)}, 500
    finally:
        s.close()
