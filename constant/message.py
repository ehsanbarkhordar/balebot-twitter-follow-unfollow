from balebot.models.messages import TemplateMessageButton


class BotMessage:
    start_conversation = "سلام.\nبه بات افزایش فالوور توییتر خوش آمدید."

    send_verify_number = "لطفا وارد لینک زیر شوید و عدد دریافتی را برای من بفرستید.\n" \
                         "{}"
    send_text_twitter = "لطفا متن توییت خود را ارسال کنید.\n" \
                        "*توجه:* ممکن است ارسال توییت کمی زمان‌بر باشد. از شکیبایی شما متشکریم"
    send_search_text = "لطفا متن مورد نظر برای جست و جو را وارد نمایید."
    success_tweet = "توییت شما با موفقیت ارسال گردید."
    fail_tweet = "متاسفانه! ارسال توییت موفق نبود."
    error = "*متاسفانه، خطایی رخ داده است. *\n" \
            " لطفا دوباره سعی کنید."
    information = "باتی برای آسانی استفاده از توییتر در پیام رسان بله\n" \
                  "برای گزارش مشکل به آیدی EhsanBarkhordar@ در بله پیام دهید."
    send_name = "لطفا نام خود را ارسال کنید."
    send_phone_number = "لطفا تلفن همراه خود را ارسال کنید."
    success_insert_user = "نام شما با موفقیت در بات ثبت شد.\n" \
                          "بزودی به صورت خودکار فرآیند فالوور گیری شروع می شود."
    fail_insert_user = "متاسفانه نام شما با موفقیت در بات ثبت نشد.\nلطفا دوباره سعی کنید."
    not_register = "شما هنوز *ثبت نام* نکرده اید!\n" \
                   "لطفا، برای شروع روی دکمه زیر کلیک کنید."
    tweet_message = "{}\n" \
                    "[لینک توییت]({})\n" \
                    "[{}]({})\n" \
                    "*لایک* : {} -- *ریتویت* : {}\n" \
                    "{}"

    retweet_text = "*ریتوییت* از {}\n"
    register_before = "*شما قبلا ثبت نام کرده اید!*"
    send_account_user_ids = "یوز آیدی اکانت(های) ویژه مورد نظر را وارد نمایید.\n" \
                            "نکته: برای وارد کردن چندین یوزر آیدی آن ها را با - از هم جدا نمایید."
    send_your_screen_name = "نام کاربری خود را وارد نمایید."
    set_spacial_account_successfully = "اکانت(های) مورد نظر با موفقیت افزوده شد."
    set_spacial_account_failure = "افزودن اکانت ویژه مورد نظر با خطا مواجه شد."
    spacial_account_exist = "اکانت ویژه مورد نظر وجود دارد."
    invalid_or_expired_token_happened = "توکن اکانت شما معتبر نمی باشد. " \
                                        "لطفا از طریق لینک زیر دوباره اقدام فرمایید."
    update_auth_was_successful = "بازیابی احراز هویت شما با *موفقیت* انجام شد."


class Keyboard:
    cancel = "لغو"
    keep_on = "تایید و ادامه"
    edit = "اصلاح میکنم"
    start = "ادامه"
    info = "راهنما"
    back = "بازگشت به منو اصلی"
    send_tweet = "ارسال تويیت"
    get_home_time_line = "خواندن تایم لاین"
    register = "ثبت نام کاربری"
    update_auth = "احراز هویت مجدد"
    search = "جستجو توییت"
    show_more = "موارد بیشتر"
    start_follow = "شروع فرآیند فالووگیری"
    add_spacial_accounts = "افزودن اکانت ویژه"
    add_spacial_accounts_with_user_id = "افزودن اکانت ویژه با یوزآیدی"


class TMB:
    info = TemplateMessageButton("راهنما")
    register = TemplateMessageButton("ثبت نام کاربری")
    update_auth = TemplateMessageButton("احراز هویت مجدد")


class State:
    help = "help"


class LogMessage:
    success_sync_user = "success_sync_user"
    max_tried_failed_to_resend = "max tried failed to resend"
    conversation_started = "conversation started"
    success_send_message = "success in send message"
    failure_send_message = "failure in send message"
    max_fail_retried = "max fails retried"


class Regex:
    score_regex = '(^[0-9]+)$|(^[۰-۹]+)$'
    quarter_regex = '^(([1-9]|1[0-6])-([1-9]|1[0-6])-([1-9]|1[0-6])-([1-9]|1[0-6]))$' \
                    '|^(([۱-۹]|۱[۰-۶])-([۱-۹]|۱[۰-۶])-([۱-۹]|۱[۰-۶])-([۱-۹]|۱[۰-۶]))$'


class UserData:
    update = "update"
    logger = "logger"
    attempt = "attempt"
    message = "message"
    succedent_message = "succedent_message"
    user_id = "user_id"
    bot = "bot"
    state_name = "state_name"
    user_peer = "user_peer"
    kwargs = "kwargs"
