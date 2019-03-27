from main.bot import updater
from main.follow_un_follow import FollowUnFollow

follow_un_follow = FollowUnFollow()
if __name__ == '__main__':
    follow_un_follow.run()
    updater.run()
