from sqlalchemy import Integer, String, DateTime, ForeignKey, DECIMAL, func
from sqlalchemy.orm import relationship, mapped_column
from model.base import Base
import uuid


class accounts(Base):
    __tablename__ = "accounts"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    account_type = mapped_column(String(255), nullable=False)
    account_number = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        default=lambda: accounts.generate_account_number(),
    )
    balance = mapped_column(DECIMAL(10, 2), nullable=False, default=0)
    created_at = mapped_column(DateTime, default=func.now())
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("users")

    @staticmethod
    def generate_account_number():
        return str(uuid.uuid4()).replace("-", "").upper()[:12]
