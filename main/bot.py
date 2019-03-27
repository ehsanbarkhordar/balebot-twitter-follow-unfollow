import asyncio

from balebot.filters import *
from balebot.handlers import *
from balebot.models.messages import *
from balebot.updater import Updater

from constant.message import *
from db.db_handler import *
from api.twitter_api import *
from main.call_backs import success_send_message, failure_send_message

updater = Updater(token=BotConfig.bot_token, loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher

logger = Logger.get_logger()


def send_message(message, peer, state_name, succedent_message=None):
    bot = dispatcher.bot
    user_data = {UserData.user_peer: peer, UserData.state_name: state_name, UserData.attempt: 1, UserData.bot: bot,
                 UserData.succedent_message: succedent_message, UserData.message: message}
    bot.send_message(message=message, peer=peer, kwargs=user_data,
                     success_callback=success_send_message, failure_callback=failure_send_message)


@dispatcher.command_handler("/start")
def start_conversation(bot, update):
    user_peer = update.get_effective_user()
    account = select_account_by_peer_id(peer_id=user_peer.peer_id)
    if account:
        buttons = [TMB.info]
        message = TemplateMessage(TextMessage(BotMessage.start_conversation), buttons)
        send_message(message=message, peer=user_peer, state_name=start_conversation.__name__)
    else:
        buttons = [TMB.register]
        message = TemplateMessage(TextMessage(BotMessage.not_register), buttons)
        send_message(message=message, peer=user_peer, state_name=start_conversation.__name__)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[Keyboard.update_auth]))
def update_authentication(bot, update):
    dispatcher.clear_conversation_data(update)
    user_peer = update.get_effective_user()
    auth = get_auth()
    dispatcher.set_conversation_data(update, "auth", auth)
    verify_link = auth['auth_url']
    message = TextMessage(BotMessage.send_verify_number.format(verify_link))
    kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message,
                     kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), verify_again),
                                                                MessageHandler(DefaultFilter(), start_conversation)])


def verify_again(bot, update):
    user_peer = update.get_effective_user()
    auth = dispatcher.get_conversation_data(update, "auth")
    oauth_verifier = update.get_effective_message().text
    final_step = final_verify(oauth_verifier=oauth_verifier, oauth_token=auth['oauth_token'],
                              oauth_token_secret=auth['oauth_token_secret'])
    result = update_account_auth(oauth_token=final_step.get("oauth_token"),
                                 oauth_token_secret=final_step.get("oauth_token_secret"),
                                 user_id=final_step.get("user_id"))
    if result == BotMessage.not_register:
        not_register_message = TextMessage(BotMessage.not_register)
        kwargs = {"message": not_register_message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(not_register_message, user_peer, success_callback=success_send_message,
                         failure_callback=failure_send_message, kwargs=kwargs)
        dispatcher.finish_conversation(update)
    elif result:
        update_auth_was_successful_message = TextMessage(BotMessage.update_auth_was_successful)
        kwargs = {"message": update_auth_was_successful_message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(update_auth_was_successful_message, user_peer, success_callback=success_send_message,
                         failure_callback=failure_send_message, kwargs=kwargs)
        dispatcher.finish_conversation(update)
    else:
        error_message = TextMessage(BotMessage.error)
        kwargs = {"message": error_message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(error_message, user_peer, success_callback=success_send_message,
                         failure_callback=failure_send_message, kwargs=kwargs)
        dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[Keyboard.register]))
def registration(bot, update):
    dispatcher.clear_conversation_data(update)
    user_peer = update.get_effective_user()
    auth = get_auth()
    dispatcher.set_conversation_data(update, "auth", auth)
    verify_link = auth['auth_url']
    message = TextMessage(BotMessage.send_verify_number.format(verify_link))
    send_message(message=message, peer=user_peer, state_name=registration.__name__)
    dispatcher.register_conversation_next_step_handler(
        update, [MessageHandler(TextFilter(), verify),
                 MessageHandler(DefaultFilter(), start_conversation)])


def verify(bot, update):
    user_peer = update.get_effective_user()
    auth = dispatcher.get_conversation_data(update, "auth")
    oauth_verifier = update.get_effective_message().text
    final_step = final_verify(oauth_verifier=oauth_verifier, oauth_token=auth['oauth_token'],
                              oauth_token_secret=auth['oauth_token_secret'])
    account = Account(peer_id=user_peer.peer_id, access_hash=user_peer.access_hash,
                      oauth_token=final_step.get("oauth_token"),
                      oauth_token_secret=final_step.get("oauth_token_secret"),
                      user_id=final_step.get("user_id"), screen_name=final_step.get("screen_name"))
    result = insert_to_table(account)
    if result is False:
        message = TextMessage(BotMessage.fail_insert_user)
        send_message(message=message, peer=user_peer, state_name=verify.__name__)
        dispatcher.finish_conversation(update)
    else:
        message = TextMessage(BotMessage.success_insert_user)
        send_message(message=message, peer=user_peer, state_name=verify.__name__)
        dispatcher.finish_conversation(update)
