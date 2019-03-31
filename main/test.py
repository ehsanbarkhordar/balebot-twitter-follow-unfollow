import random

from api.twitter_api import *
from db.db_handler import select_account_by_peer_id

#
foo = ['a', 'b', 'c', 'd', 'a']
a=set()
a.add("a")
a.add("b")
a.add("c")
a=list(a)
foo=set(foo)
print(foo)
print(random.choices(foo, k=2))

# account = select_account_by_peer_id("201707397")
# res = get_user_suggestions_statuses_by_slug(account.oauth_token, account.oauth_token_secret, "tv")
# res = get_user_suggestions(account.oauth_token, account.oauth_token_secret, lang="fa")
# print(res)
# for i in res:
#     slug = i.get("slug")
#     res = get_user_suggestions_statuses_by_slug(account.oauth_token, account.oauth_token_secret, "سرگرمی")
#     print(res)
# user_ids_list = set()
# account_time_line = get_home_time_line(account.oauth_token, account.oauth_token_secret, account.user_id, count=3)
# for status in account_time_line:
#     lang = status.get('lang')
#     if lang == 'fa':
#         purpose_user = status.get('user')
#         purpose_user_id = purpose_user.get('id')
#         purpose_user_timeline = get_home_time_line(account.oauth_token, account.oauth_token_secret, purpose_user_id,
#                                                    count=20)
#         for purpose_status in purpose_user_timeline:
#             purpose_lang = purpose_status.get('lang')
#             if purpose_lang == 'fa':
#                 extended_user = status.get('user')
#                 extended_user_id = extended_user.get('id')
#                 user_ids_list.add(extended_user_id)
#
# print(account_time_line)
