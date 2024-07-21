from sqlalchemy import Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, mapped_column
from model.base import Base


class Transactions(Base):
    __tablename__ = "transactions"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey("accounts.id"))
    to_account_id = mapped_column(Integer, ForeignKey("accounts.id"))
    amount = mapped_column(DECIMAL(10, 2), nullable=False)
    type = mapped_column(String(255))
    description = mapped_column(String(255))
    created_at = mapped_column(DateTime, default=func.now())
