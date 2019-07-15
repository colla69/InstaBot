from bot.context import *
from time import sleep
from bot.user import User
import threading
from datetime import datetime
from bot.humanized_bot import HumanizedBot


def do_follow_followers():
    while True:
        user.follow_followers()
        sleep(18000)


def do_follow_followers():
    while True:
        user.follow_followers()
        sleep(18000)


start = datetime.now()

user = HumanizedBot(psw4()[0], psw4()[1])
user.login()

job_threads = [
                threading.Thread(target=user.follow_n_like),
                threading.Thread(target=user.start_scheduler),
                threading.Thread(target=do_follow_followers),
              ]
[job_thread.start() for job_thread in job_threads]
[job_thread.join() for job_thread in job_threads]

end = datetime.now()
print("duration ", end="")
print(end-start)

"""
user.login()
sleep(2)
user.like_following()

log = Logger()
instagram = Instagram(2)
instagram.with_credentials(psw()[0], psw()[1], 'path/to/cache/folder')
instagram.login()
user = psw()[0]
sleep(2)
account = instagram.get_account(user)
print(account)

sleep(1)
count_following = account.follows_count
follow = instagram.get_following_hashtags(account.identifier, 2, 2, delayed=True) # Get 150 followers of 'kevin', 100 a time with random delay between requests
follow_accounts = follow["accounts"]
print(follow_accounts)
random.shuffle(follow_accounts)
for acc in follow_accounts:
    sleep(1)
    print(acc.name)
    posts = instagram.get_medias(acc.name, 20)
    print(posts)
    break

followers = instagram.get_followers(account.identifier, 150, 100, delayed=True) # Get 150 followers of 'kevin', 100 a time with random delay between requests
sleep(1)
followers_accounts = followers["accounts"]
random.shuffle(followers_accounts)
for acc in followers_accounts:
    sleep(1)
    acc = instagram.get_account_by_id(acc.identifier)
    print(" {} follows me: {} ".format(acc.username, acc.follows_viewer))
    if not acc.follows_viewer:
        instagram.follow(acc.identifier)
        log.log("following: {}".format(acc.username))


sleep(1)
following = instagram.get_following(account.identifier, 150, 100, delayed=True)
for following_user in following['accounts']:
    print(following_user)

sleep(2)
followers = instagram.get_followers(account.identifier, 150, 100, delayed=True) # Get 150 followers of 'kevin', 100 a time with random delay between requests
for follower in followers['accounts']:
    print(follower)
"""