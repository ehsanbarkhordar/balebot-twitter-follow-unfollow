import logging
import os

try:
    from local_config import LocalConfig
    api_key = LocalConfig.consumer_api_key
    api_secret = LocalConfig.consumer_api_secret
    token = LocalConfig.bot_token
    db_user = LocalConfig.db_user
    db_pass = LocalConfig.db_pass
    db_host = LocalConfig.db_host
    db_port = LocalConfig.db_port
    db_name = LocalConfig.db_name

except ImportError:
    api_key = ''
    api_secret = ''
    token = ''
    db_user = ''
    db_pass = ''
    db_host = ''
    db_port = ''
    db_name = ''


class BotConfig:
    bot_token = os.environ.get('TOKEN', token)
    resending_max_try = int(os.environ.get('RESENDING_MAX_TRY', 3))
    consumer_api_key = os.environ.get('API_KEY', api_key)
    consumer_api_secret = os.environ.get('API_SECRET', api_secret)
    twitter_user_link_by_id = os.environ.get('TWITTER_USER_LINK_BY_ID', "https://twitter.com/intent/user?user_id=")
    max_follow_per_round = int(os.environ.get('MAX_FOLLOW_PER_ROUND', 30))
    max_un_follow_per_round = int(os.environ.get('MAX_UN_FOLLOW_PER_ROUND', 100))
    loop_delay = float(os.environ.get('LOOP_DELAY', 1.5))
    use_gray_log = os.environ.get('USE_GRAY_LOG', "0")
    source = os.environ.get('LOG_SOURCE', "bot_source")
    gray_log_host = os.environ.get('GRAY_LOG_HOST', "172.30.41.67")
    gray_log_port = int(os.environ.get('GRAY_LOG_PORT', 12201))
    log_level = int(os.environ.get('LOG_LEVEL', logging.DEBUG))
    log_facility_name = os.environ.get('LOG_FACILITY_NAME', "python_bale_bot")


class DatabaseConfig:
    db_string_main = 'postgresql://{}:{}@{}:{}/{}'
    db_string = db_string_main.format(os.environ.get('POSTGRES_USER', db_user),
                                      os.environ.get('POSTGRES_PASSWORD', db_pass),
                                      os.environ.get('POSTGRES_HOST', db_host),
                                      os.environ.get('POSTGRES_PORT', db_port),
                                      os.environ.get('POSTGRES_DB', db_name))
