from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, mapped_column
from model.base import Base
from flask_login import UserMixin
import bcrypt


class users(Base, UserMixin):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(255), unique=True, nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    password_hash = mapped_column(String(225), nullable=False)
    created_at = mapped_column(DateTime, default=func.now())
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    accounts = relationship("accounts", back_populates="user")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )
