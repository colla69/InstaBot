from bot.context import *
import random
from bot.utils import *
from time import sleep


class User:

    def __init__(self, username, psw):
        self.username = username
        self.password = psw
        self.instagram = Instagram()
        self.path = os.path.dirname(os.path.realpath(__file__)) + "/" + self.username + "/"
        self.logger = Logger(self.path)
        self.account = None
        self.following = []
        self.following_names = []

    def add_following(self, user_id):
        """
        follow a new user by ID

        :param user_id: user to follow
        :return:
        """
        sleep(360)  # too much follows => function ban
        self.following.append(user_id)
        return perform_with_ran_delay(self.instagram.follow, user_id)

    def load_account(self):
        self.account = self.instagram.get_account(self.username)

    """########################################## instagram interactions ############################################"""

    def login(self):
        self.instagram.with_credentials(self.username, self.password, self.username)
        self.instagram.login()
        perform_with_ran_delay(self.load_account)
        self.logger.log( "-----  logged in! as {}  -----".format(self.username))
        perform_with_ran_delay(self.load_following)

    def load_following(self):
        self.logger.log("loading followed accounts... ", end="")
        count_following = self.account.follows_count
        follow = self.instagram.get_following(self.account.identifier, count_following, 10, delayed=True)
        for f in follow["accounts"]:
            self.following.append(f.identifier)
            self.following_names.append(f.username)
        # for f in self.following_names:
        #    print(f)
        self.logger.log( "loaded {} followers ".format(len(self.following_names)))
        self.logger.log("done!")

    def is_user_following(self, user_id):
        """
        checks if user is following a given user

        :param user_id: user you want to check
        :return: True if following
        """
        return user_id in self.following

    def follow_followers(self):
        """
        follow user's followers, if not already following

        :return: list of Media
        """
        self.logger.log("starting follow_followers...")
        follow = perform_with_ran_delay(self.instagram.get_followers, self.account.identifier, 150, 15, delayed=True)
        for acc in follow["accounts"]:
            try:
                try:
                    # print("{} follows me, do I follow him ? > {} ".format(acc.username,self.is_user_following(acc.identifier)))
                    if not self.is_user_following(acc.identifier):
                        if self.add_following(acc.identifier):
                            self.logger.log("following: {}".format(acc.username))
                        else:
                            self.logger.log("follow not working at the moment")
                except Exception as e:
                    print(e)
                    self.logger.log(str(e))
                    continue
            finally:
                sleep(3)

    def follow_following_followers(self):
        """
        follow the users, the people you are following follow
        if not alreadyidentifier

        :return: list of Media
        """
        self.logger.log("starting follow_following_followers...")
        follows_accounts = self.following
        random.shuffle(follows_accounts)
        for acc in follows_accounts:
            try:
                try:
                    followw = perform_with_ran_delay(self.instagram.get_followers, acc, 150, 15,
                                                     delayed=True)
                    accountstofollow = followw["accounts"]
                    random.shuffle(accountstofollow)
                    if len(accountstofollow) > 10:
                        accountstofollow = accountstofollow[:10]
                    for ac in accountstofollow:
                        if not self.is_user_following(ac.identifier):
                            self.add_following(ac.identifier)
                            self.logger.log("following: {}".format(ac.username))
                except Exception as e:
                    print(e)
                    self.logger.log(str(e))
            finally:
                sleep(3)

    def like_following(self):
        """
        like the posts from the people the user follows

        :return: list of Media
        """
        self.logger.log("starting like_following...")
        count_following = self.account.follows_count
        follows_accounts = self.following
        random.shuffle(follows_accounts)
        for acc in follows_accounts:
            acc = perform_with_ran_delay(self.instagram.get_account_by_id, acc)
            self.logger.log(" {} > {} posts".format(acc.username, acc.media_count))
            if acc.media_count > 0:

                posts = perform_with_ran_delay(self.instagram.get_medias, acc.username, 50)
                if posts:
                    for m in posts:
                        try:
                            perform_with_ran_delay(self.instagram.like, m.identifier)
                            self.logger.log("liking 1 post from "+acc.username)
                            random_delay()
                        except Exception as e:
                            self.logger.log("skipping 1 post from "+acc.username)
                            self.logger.log(e)
                            random_delay()
                            continue
