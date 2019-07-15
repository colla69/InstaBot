from bot.context import *
import threading
from apscheduler.schedulers.background import BlockingScheduler
from bot.user import User
from time import sleep
from datetime import datetime

scheduler = BlockingScheduler()
job = None
# user = User(psw3()[0], psw3()[1])
user = User(psw2()[0], psw2()[1])


def work():
    user.logger.log("starting bot... ")
    user.login()
    start = datetime.now()

    threads = [threading.Thread(target=user.follow_following_followers),
               threading.Thread(target=user.like_following),
               threading.Thread(target=user.follow_followers),
               ]

    [x.start() for x in threads]
    [x.join() for x in threads]

    end = datetime.now()
    user.logger.log("duration ", end="")
    user.logger.log(end - start)


def start_job():
    global job
    scheduler.add_job(work, 'interval', seconds=18000)
    work()
    try:
        scheduler.start()
    except Exception as e:
        print(e)


start_job()

