import os
from datetime import datetime
import random
from time import sleep


def random_delay():
    microsec = random.uniform(1.5, 4.0)
    sleep(microsec)


def perform_with_ran_delay(fun, *args, **kwargs):
    random_delay()
    return fun(*args, **kwargs)


class Logger:
    def __init__(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
        self.path = path + "log.txt"

    def log(self, line, *args, **kwargs):
        file = open(self.path, 'a', encoding="utf-8")
        line = "{} --- {}".format(datetime.now(), line)
        file.write("\n"+line)
        print(line, *args, **kwargs)
        file.close()
