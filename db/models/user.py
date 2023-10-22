from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String

from db.models.base import Base


class Tokens(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    token_hhid = Column(String)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    registration_completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(),
                        nullable=False, onupdate=datetime.utcnow())
    is_admin = Column(Boolean, nullable=True)


# TODO
class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    created_at = Column(Date, default=datetime.utcnow(), nullable=False)
    updated_at = Column(Date, default=datetime.utcnow(),
                        nullable=False, onupdate=datetime.utcnow())

    # TODO subscription_type = Column(enum[SubscriptionEnum], nullable=True)
