from bot.context import *
import threading

job_thread = None


class HumanScheduler:

    def __init__(self, logger):
        self.actions = []
        self.cancel = False
        self.pause = False
        self.logger = logger

    def add_action(self, actionname, action, *args, **kwargs):
        a = Action(actionname, action)
        a.args = args
        a.kwargs = kwargs
        self.actions.append(a)

    def perform_action(self, action):
        try:
            return action.action(*action.args, **action.kwargs)
        except Exception as e:
            print("!!! exception performing action in scheduler !!!")
            print(type(e))
            print(e)
            print(action)

    def start(self):
        sleep(30)  # wait for some actions to be added before starting the scheduler
        self.logger.log("-----  scheduler started -----")
        while not self.cancel:
            if not self.actions:
                self.logger.log("no actions .. sleeping 1 minute")
                sleep(60)
            count = 0
            for a in self.actions:
                if not self.pause:
                    count += 1
                    if count % 30 == 0:
                        # print("trying to be human at {}".format(count))
                        self.be_human()  # eventually make pauses to act human like ;)
                    random_delay()  # take a mandatory pause between actions
                    # print("performing {}".format(a))
                    self.perform_action(a)
                else:
                    self.logger.log("scheduler paused ...")
                self.actions.remove(a)
            self.logger.log("scheduler sleeping before restarting routine...")
            sleep(100)
            self.logger.log("-----  restarting routine -----")
        self.stop()

    def stop(self):
        self.cancel = True

    def pause(self):
        self.pause = True

    def resume(self):
        self.pause = False

    def take_a_leak(self):
        """
        take a 3 min pause
        :return:
        """
        self.logger.log("scheduler is taking a leak")
        sleep(180)

    def take_a_dump(self):
        """
        take a 10 min pause
        :return:
        """
        self.logger.log("scheduler is taking a dump")
        sleep(600)

    def take_a_nap(self):
        """
        take a 1 hour pause
        :return:
        """
        self.logger.log("scheduler is napping... zzzzzz...")
        sleep(3600)

    def be_human(self):
        ran = random.uniform(0, 100)
        if ran > 95:
            self.take_a_nap()
        elif ran > 90:
            self.take_a_dump()
        elif ran > 65:
            self.take_a_leak()


class Action:

    def __init__(self, action_name, action):
        self.action = action
        self.args = None
        self.kwargs = None
        self.action_name = action_name

    def __str__(self):
        return """
        Action info:
        name {}
        args {}
        kwargs {}""".format(self.action_name, self.args, self.kwargs)
