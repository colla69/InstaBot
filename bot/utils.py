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
    def __init__(self,logfile):
        self.path = logfile

    def log(self, line, *args, **kwargs):
        file = open(self.path, 'a', encoding="utf-8")
        file.write("\n{} --- {}".format(datetime.now(), line))
        print(line, *args, **kwargs)
        file.close()
