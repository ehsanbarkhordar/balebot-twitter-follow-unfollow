import logging
import os

from local_config import LocalConfig


class BotConfig:
    bot_token = os.environ.get('TOKEN', LocalConfig.bot_token)
    resending_max_try = int(os.environ.get('RESENDING_MAX_TRY', 3))
    check_interval = float(os.environ.get('CHECK_INTERVAL', 300))
    consumer_api_key = os.environ.get('API_KEY', LocalConfig.consumer_api_key)
    consumer_api_secret = os.environ.get('API_SECRET', LocalConfig.consumer_api_secret)
    twitter_user_link_by_id = os.environ.get('TWITTER_USER_LINK_BY_ID', "https://twitter.com/intent/user?user_id=")
    max_follow_per_round = int(os.environ.get('MAX_FOLLOW_PER_ROUND', 20))
    max_un_follow_per_round = int(os.environ.get('MAX_UN_FOLLOW_PER_ROUND', 5))
    loop_delay = float(os.environ.get('LOOP_DELAY', 1.5))
    use_gray_log = os.environ.get('USE_GRAY_LOG', "0")
    source = os.environ.get('LOG_SOURCE', "bot_source")
    gray_log_host = os.environ.get('GRAY_LOG_HOST', "172.30.41.67")
    gray_log_port = int(os.environ.get('GRAY_LOG_PORT', 12201))
    log_level = int(os.environ.get('LOG_LEVEL', logging.DEBUG))
    log_facility_name = os.environ.get('LOG_FACILITY_NAME', "python_bale_bot")


class DatabaseConfig:
    db_string_main = 'postgresql://{}:{}@{}:{}/{}'
    db_string = db_string_main.format(os.environ.get('POSTGRES_USER', LocalConfig.db_user),
                                      os.environ.get('POSTGRES_PASSWORD', LocalConfig.db_pass),
                                      os.environ.get('POSTGRES_HOST', LocalConfig.db_host),
                                      os.environ.get('POSTGRES_PORT', LocalConfig.db_port),
                                      os.environ.get('POSTGRES_DB', LocalConfig.db_name))
