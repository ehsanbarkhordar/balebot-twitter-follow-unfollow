import asyncio
import random

from balebot.models.base_models import Peer
from balebot.models.constants.peer_type import PeerType
from balebot.models.messages import TextMessage, TemplateMessage
from main import bot
from api.twitter_api import *
from constant.message import *
from db.db_handler import *


class FollowUnFollow:
    def __init__(self):

        self.logger = Logger.get_logger()
        self.async_loop = asyncio.get_event_loop()
        self.database_handler = engine
        self.check_next = True
        self.running = True
        self.perform_check_failure_counter = 0
        self.total_send_failure_counter = 0
        self.max_follow_per_round = BotConfig.max_follow_per_round
        self.bot = bot
        self.consumer_key = BotConfig.consumer_api_key
        self.consumer_secret = BotConfig.consumer_api_secret

    def user_api_keys_validated(self, user):
        result = get_home_time_line(user.oauth_token, user.oauth_token_secret, user.user_id)
        if isinstance(result, list):
            return True
        if result.error_code == 401:
            general_message = TextMessage(BotMessage.invalid_or_expired_token_happened)
            buttons = [TMB.update_auth]
            message = TemplateMessage(general_message, buttons)
            user_peer = Peer(PeerType.user, user.peer_id, user.access_hash)
            self.bot.send_message(message=message, peer=user_peer, state_name=self.user_api_keys_validated.__name__)
            return False
        if result.error_code == 403:
            return False

    def sync_friends(self, account):
        print("start_sync_data")
        cursor = -1
        following_ids = []
        while cursor != 0:
            response_dictionary = get_friends_ids(account.oauth_token, account.oauth_token_secret,
                                                  account.user_id, cursor)
            if not response_dictionary:
                return False
            cursor = response_dictionary.get("next_cursor")
            response_ids = response_dictionary.get("ids")
            following_ids += response_ids
        for user_id in following_ids:
            friend = Friend(user_id=user_id, account_user_id=account.user_id)
            insert_to_table(friend)
        sync_account(account)
        self.logger.info(LogMessage.success_sync_user)

    def get_random_ids_to_follow(self, account):
        random_ids_for_follow = []
        try:
            account_time_line = get_home_time_line(account.oauth_token, account.oauth_token_secret, account.user_id,
                                                   count=5)
            for status in account_time_line:
                lang = status.get('lang')
                if lang == 'fa':
                    purpose_user = status.get('user')
                    purpose_user_id = purpose_user.get('id')
                    purpose_user_timeline = get_home_time_line(account.oauth_token, account.oauth_token_secret,
                                                               purpose_user_id,
                                                               count=20)

                    for purpose_status in purpose_user_timeline:
                        purpose_lang = purpose_status.get('lang')
                        if purpose_lang == 'fa':
                            extended_user = status.get('user')
                            extended_user_id = extended_user.get('id')
                            random_ids_for_follow.append(extended_user_id)
        except Exception as e:
            print(e)
            return False
        random.choices(random_ids_for_follow, k=50)
        random_ids_for_follow = set(random_ids_for_follow)
        self.logger.info("get_random_ids_to_follow")
        return random_ids_for_follow

    def un_follow(self, account):
        old_friends = select_old_friends(account.user_id, limit=BotConfig.max_un_follow_per_round)
        if old_friends:
            for friend in old_friends:
                twitter = Twython(self.consumer_key, self.consumer_secret, account.oauth_token,
                                  account.oauth_token_secret)
                try:
                    twitter.destroy_friendship(user_id=friend.user_id)
                    print("was unfollow successfully, user_id", friend.user_id)
                    unfollow_friend(friend)
                except TwythonError as e:
                    print(e)
                    print(e.args)
                    print("user_id: ", friend.user_id, "was unfollow failure")
                    break

    def follow(self, account):
        random_ids_for_follow = self.get_random_ids_to_follow(account)
        print("random_ids_for_follow: ", random_ids_for_follow)
        if random_ids_for_follow:
            for new_id in random_ids_for_follow:
                if select_friend_by_user_id(account.user_id, new_id) or account.user_id == new_id:
                    print("new_id", new_id, "is friend now")
                else:
                    twitter = Twython(self.consumer_key, self.consumer_secret, account.oauth_token,
                                      account.oauth_token_secret)
                    try:
                        twitter.create_friendship(user_id=new_id)
                        print("has been friend ,user_id: ", new_id)
                        friend = Friend(user_id=new_id, account_user_id=account.user_id, unfollow_permission=True)
                        insert_to_table(friend)
                    except TwythonError as e:
                        print("friendship was failure, user_id: ", new_id)
                        print(e.args)
                        if e.error_code == 403:
                            break

    def run(self):
        if self.running:
            if self.check_next and self.database_handler.connect():
                self.check_next = False
                accounts = select_accounts()
                if accounts:
                    for account in accounts:
                        if self.user_api_keys_validated(account):
                            if not account.is_sync:
                                self.sync_friends(account)
                            self.check_next = False
                            self.follow(account)
                            self.un_follow(account)
                            self.check_next = True
                        else:
                            self.check_next = True
                else:
                    self.check_next = True
            else:
                self.logger.info("db connected: {}".format("True", extra={"tag": "info"}))
                self.logger.info("check_next: {}".format(self.check_next), extra={"tag": "info"})
            random_time_interval = random.randint(200, 1500)
            self.async_loop.call_later(50, self.run)

    def stop(self):
        self.running = False
        self.logger.warning("follow-un-follow stopped", extra={"tag": "warning"})
