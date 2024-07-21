from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
from connectors.connectors import connection
from model.accounts import accounts
from model.transaction import Transactions
from decimal import Decimal


transaction_routes = Blueprint("transaction_routes", __name__)


@transaction_routes.route("/transaction", methods=["GET"])
@login_required
def get_transactions():
    Session = sessionmaker(connection)
    session = Session()
    try:
        user_accounts = session.query(accounts).filter_by(user_id=current_user.id).all()
        account_ids = [account.id for account in user_accounts]
        transactions = (
            session.query(Transactions)
            .filter(
                (Transactions.from_account_id.in_(account_ids))
                | (Transactions.to_account_id.in_(account_ids))
            )
            .all()
        )
        transaction_list = [
            {
                "id": transaction.id,
                "from_account_id": transaction.from_account_id,
                "to_account_id": transaction.to_account_id,
                "amount": transaction.amount,
                "type": transaction.type,
                "description": transaction.description,
                "created_at": transaction.created_at,
            }
            for transaction in transactions
        ]
        return jsonify(transaction_list), 200
    except Exception as e:
        session.rollback()
        return {"message": "Error fetching transactions", "error": str(e)}, 500
    finally:
        session.close()


@transaction_routes.route("/transaction/<id>", methods=["GET"])
@login_required
def get_transaction_by_id(id):
    Session = sessionmaker(connection)
    session = Session()
    try:
        transaction = session.query(Transactions).filter_by(id=id).first()
        if transaction is None:
            return {"message": "Transaction not found"}, 404
        user_accounts = session.query(accounts).filter_by(user_id=current_user.id).all()
        account_ids = [account.id for account in user_accounts]
        if (
            transaction.from_account_id not in account_ids
            and transaction.to_account_id not in account_ids
        ):
            return {"message": "Unauthorized access to transaction"}, 403

        transaction_detail = {
            "id": transaction.id,
            "from_account_id": transaction.from_account_id,
            "to_account_id": transaction.to_account_id,
            "amount": transaction.amount,
            "type": transaction.type,
            "description": transaction.description,
            "created_at": transaction.created_at,
        }
        return jsonify(transaction_detail), 200
    except Exception as e:
        session.rollback()
        return {"message": "Error fetching transaction", "error": str(e)}, 500
    finally:
        session.close()


@transaction_routes.route("/transaction", methods=["POST"])
@login_required
def create_transaction():
    try:
        from_account_id = int(request.form["from_account_id"])
        to_account_id = request.form.get("to_account_id", type=int)
        amount = Decimal(request.form["amount"])
        transaction_type = request.form["type"]
        description = request.form["description"]

        if not from_account_id or not amount or not transaction_type:
            return {"message": "Missing required fields"}, 400

        Session = sessionmaker(connection)
        session = Session()
        from_account = (
            session.query(accounts)
            .filter_by(id=from_account_id, user_id=current_user.id)
            .first()
        )
        if not from_account:
            return {"message": "Unauthorized access to from_account"}, 403

        if transaction_type == "withdrawal":
            if from_account.balance < amount:
                return {"message": "Insufficient balance"}, 400
            from_account.balance -= amount

        elif transaction_type == "transfer":
            if not to_account_id:
                return {"message": "Missing to_account_id for transfer"}, 400
            to_account = session.query(accounts).filter_by(id=to_account_id).first()
            if not to_account:
                return {"message": "Invalid to_account_id"}, 400

            if from_account.balance < amount:
                return {"message": "Insufficient balance"}, 400
            from_account.balance -= amount
            to_account.balance += amount

        else:
            return {"message": "Invalid transaction type"}, 400
        new_transaction = Transactions(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            type=transaction_type,
            description=description,
        )
        session.add(new_transaction)
        session.commit()

        return {"message": "Transaction successful"}, 201

    except Exception as e:
        session.rollback()
        return {"message": "Error processing transaction", "error": str(e)}, 500

    finally:
        session.close()
