import datetime
from balebot.utils.logger import Logger
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from db.models import Friend, Account, Base
from main_config import DatabaseConfig

engine = create_engine(DatabaseConfig.db_string)
meta = MetaData(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()
logger = Logger.get_logger()


def db_persist(func):
    def persist(*args, **kwargs):
        result = func(*args, **kwargs)
        try:
            session.commit()
            logger.info("success calling db func: " + func.__name__)
            return result
        except SQLAlchemyError as e:
            logger.error(e.args)
            session.rollback()
            return False

    return persist


@db_persist
def select_accounts():
    return session.query(Account).all()


@db_persist
def select_account_by_peer_id(peer_id):
    return session.query(Account).filter(Account.peer_id == peer_id).one_or_none()


@db_persist
def select_account_by_screen_name(screen_name):
    return session.query(Account).filter(Account.screen_name == screen_name).one_or_none()


@db_persist
def select_recent_friends(user_id, limit=15):
    return session.query(Friend).filter(Friend.account_user_id == user_id).order_by(Friend.user_id.desc()).limit(
        limit).all()


@db_persist
def select_old_friends(user_id, limit):
    expired_datetime = datetime.datetime.now() - datetime.timedelta(days=2)
    return session.query(Friend).filter(
        Friend.account_user_id == user_id,
        Friend.unfollow_permission.is_(True), Friend.unfollow_datetime.is_(None),
        Friend.follow_datetime < expired_datetime) \
        .order_by(Friend.follow_datetime).limit(limit).all()


@db_persist
def select_from_friends(user_id, limit):
    return session.query(Friend).filter(
        Friend.account_user_id == user_id, Friend.unfollow_datetime.is_(None)) \
        .order_by(Friend.follow_datetime).limit(limit).all()


@db_persist
def unfollow_friend(friend: Friend):
    friend.unfollow_datetime = datetime.datetime.now()


@db_persist
def insert_to_table(table_obj):
    session.add(table_obj)


@db_persist
def delete_from_table(table_object):
    session.delete(table_object)


@db_persist
def insert_or_update(table_object):
    return session.merge(table_object)


@db_persist
def sync_account(account: Account):
    account.is_sync = True


@db_persist
def select_friend_by_user_id(user_id, account_user_id):
    return session.query(Friend).filter(Friend.account_user_id == account_user_id,
                                        Friend.user_id == user_id).one_or_none()


@db_persist
def update_account_auth(oauth_token, oauth_token_secret, account: Account):
    account.oauth_token = oauth_token
    account.oauth_token_secret = oauth_token_secret
