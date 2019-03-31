from twython import Twython, TwythonError

from main_config import BotConfig

consumer_key = BotConfig.consumer_api_key
consumer_secret = BotConfig.consumer_api_secret


def api_error_handler(fuc):
    def handler(*args, **kwargs):
        try:
            result = fuc(*args, **kwargs)
            return result
        except TwythonError as e:
            print(e.args)
            return e

    return handler


@api_error_handler
def get_auth():
    twitter = Twython(consumer_key, consumer_secret)
    auth = twitter.get_authentication_tokens()
    return auth


@api_error_handler
def final_verify(oauth_verifier, oauth_token, oauth_token_secret):
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    final_step = twitter.get_authorized_tokens(oauth_verifier)
    return final_step


@api_error_handler
def get_home_time_line(oauth_token, oauth_token_secret, user_id, count=5, trim_user=True):
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    result = twitter.get_home_timeline(user_id=user_id, count=count, trim_user=trim_user)
    return result


@api_error_handler
def create_friendship(oauth_token, oauth_token_secret, user_id):
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    result = twitter.create_friendship(user_id=user_id)
    print("user_id: ", user_id, "was followed successfully")
    return result


@api_error_handler
def destroy_friendship(oauth_token, oauth_token_secret, user_id):
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    result = twitter.destroy_friendship(user_id=user_id)
    print("user_id: ", user_id, "was unfollowed successfully")
    return result


@api_error_handler
def get_followers_ids(oauth_token, oauth_token_secret, user_id, count=5000):
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    result = twitter.get_followers_ids(user_id=user_id, count=count)
    return result


@api_error_handler
def get_followers_list(oauth_token, oauth_token_secret, user_id, count=20):
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    result = twitter.get_followers_list(user_id=user_id, count=count)
    return result


@api_error_handler
def get_friends_ids(oauth_token, oauth_token_secret, user_id, count=500, cursor=-1):
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    result = twitter.get_friends_ids(user_id=user_id, count=count, cursor=cursor)
    return result


@api_error_handler
def show_user(oauth_token, oauth_token_secret, user_id, screen_name):
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    result = twitter.show_user(user_id=user_id, screen_name=screen_name)
    return result


@api_error_handler
def get_user_suggestions_statuses_by_slug(oauth_token, oauth_token_secret, slug):
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    result = twitter.get_user_suggestions_statuses_by_slug(slug=slug)
    return result


@api_error_handler
def get_user_suggestions(oauth_token, oauth_token_secret, lang):
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    result = twitter.get_user_suggestions(lang=lang)
    return result
