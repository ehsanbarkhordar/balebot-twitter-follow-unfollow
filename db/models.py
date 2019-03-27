from datetime import datetime

from sqlalchemy import Column, BigInteger, ForeignKey, Boolean, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    peer_id = Column(String, nullable=False)
    access_hash = Column(String, nullable=False)
    oauth_token = Column(String, nullable=False)
    oauth_token_secret = Column(String, nullable=False)
    user_id = Column(BigInteger, nullable=False, primary_key=True)
    screen_name = Column(String, nullable=False)
    is_sync = Column(Boolean, default=False)

    def __init__(self, peer_id, access_hash, oauth_token, oauth_token_secret, user_id, screen_name):
        self.peer_id = peer_id
        self.access_hash = access_hash
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.user_id = user_id
        self.screen_name = screen_name

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class Friend(Base):
    __tablename__ = 'friends'
    user_id = Column(BigInteger, primary_key=True)
    account_user_id = Column(BigInteger, ForeignKey('accounts.user_id'), primary_key=True)
    follow_datetime = Column(DateTime)
    unfollow_datetime = Column(DateTime)
    unfollow_permission = Column(Boolean, default=False)
    follow_back = Column(Boolean, default=False)

    def __init__(self, user_id, account_user_id, follow_datetime=datetime.now(), unfollow_permission=False):
        self.user_id = user_id
        self.account_user_id = account_user_id
        self.follow_datetime = follow_datetime
        self.unfollow_permission = unfollow_permission

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
