from balebot.utils.logger import Logger

from constant.message import UserData, LogMessage
from main_config import BotConfig

logger = Logger.get_logger()


def success_send_message(response, user_data):
    user_data = user_data[UserData.kwargs]
    user_peer = user_data[UserData.user_peer]
    state_name = user_data[UserData.state_name]
    succedent_message = user_data[UserData.succedent_message]
    extra = {UserData.user_id: user_peer.peer_id, UserData.state_name: state_name, "tag": "info"}
    logger.info(LogMessage.success_send_message.format(state_name), extra=extra)
    if succedent_message:
        bot = user_data[UserData.bot]
        user_data[UserData.succedent_message] = None
        bot.send_message(message=succedent_message, peer=user_peer, kwargs=user_data,
                         success_callback=success_send_message,
                         failure_callback=failure_send_message)


def failure_send_message(response, user_data):
    user_data = user_data[UserData.kwargs]
    user_peer = user_data[UserData.user_peer]
    state_name = user_data[UserData.state_name]
    attempt = user_data[UserData.attempt]
    bot = user_data[UserData.bot]
    message = user_data[UserData.message]
    user_data[UserData.attempt] += 1
    extra = {UserData.user_id: user_peer.peer_id, UserData.state_name: state_name, "tag": "error"}
    logger.error(LogMessage.failure_send_message.format(state_name, attempt), extra=extra)
    if user_data[UserData.attempt] < BotConfig.resending_max_try:
        bot.send_message(message=message, peer=user_peer, kwargs=user_data,
                         success_callback=success_send_message,
                         failure_callback=failure_send_message)
    else:
        extra = {UserData.user_id: user_peer.peer_id, UserData.state_name: state_name, "tag": "error"}
        logger.error(LogMessage.max_tried_failed_to_resend.format(state_name), extra=extra)
