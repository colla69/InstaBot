from bot.context import *
from bot.humanScheduler import HumanScheduler


class HumanizedBot:

    def __init__(self, username, passw):
        self.username = username
        self.password = passw
        self.path = os.path.dirname(os.path.realpath(__file__)) + "/" + self.username + "/"
        self.logger = Logger(self.path)
        self.hs = HumanScheduler(self.logger)
        self.instagram = Instagram()
        self.account = None
        self.following = []
        self.following_names = []

    def make_routine(self):
        self.logger.log("-----  loading routine -----")
        self.follow_n_like()

    def start_scheduler(self):
        self.logger.log("-----  starting scheduler -----")
        self.hs.start()

    def follow_n_like(self):
        """
            follow the users, the people you are following follow
            if not already following and like some of their posts

            :return: list of Media
        """
        self.logger.log("loading follow 'n' like ...")
        follows_accounts = self.following
        random.shuffle(follows_accounts)
        for acc in follows_accounts:
            try:
                try:
                    followw = self.instagram.get_followers(acc, 50, 15, delayed=True)
                    accountstofollow = followw["accounts"]
                    random.shuffle(accountstofollow)
                    if len(accountstofollow) > 10:
                        accountstofollow = accountstofollow[:10]
                    for ac in accountstofollow:
                        if not self.is_user_following(ac.identifier):
                            self.add_following(ac.identifier, ac.username)
                            sleep(10)  # wait before downloading posts
                            self.like_post_by_user(ac.username)

                except Exception as e:
                    self.logger.log(str(e))
                    random_delay()
                    random_delay()
            finally:
                sleep(20)

    def follow_followers(self):
        """
        follow user's followers, if not already following

        :return: list of Media
        """
        self.logger.log("starting follow_followers...")
        follow = self.instagram.get_followers( self.account.identifier, 150, 15, delayed=True)
        for acc in follow["accounts"]:
            try:
                if not self.is_user_following(acc.identifier):
                    self.add_following(acc.identifier, acc.username)
            except Exception as e:
                print(e)
                self.logger.log(str(e))
                continue

    def like_post_by_user(self, username):
        posts = self.instagram.get_medias(username, 50)
        if posts:
            for m in posts:
                try:
                    self.logger.log("adding 1 post from " + username)
                    self.hs.add_action("like", self.like, m.identifier, username)
                    random_delay()
                except Exception as e:
                    self.logger.log("problem while adding posts from " + username)
                    self.logger.log(e)
                    random_delay()
                    continue

    def like(self, media_id, username):
        self.logger.log("liking 1 post from " + username)
        self.instagram.like(media_id)

    def login(self):
        self.instagram.with_credentials(self.username, self.password)
        self.instagram.login()
        perform_with_ran_delay(self.load_account)
        self.logger.log( "-----  logged in! as {}  -----".format(self.username))
        perform_with_ran_delay(self.load_following)

    def add_following(self, user_id, username):
        """
        follow a new user by ID

        :param user_id: user to follow
        :param username: username
        :return:
        """
        self.logger.log("adding follow action for user: {}".format(username))
        self.hs.add_action("follow", self.follow, user_id, username)

    def follow(self, user_id, username):
        self.following.append(user_id)
        self.instagram.follow(user_id)
        self.logger.log("following: {}".format(username))

    def load_account(self):
        self.account = self.instagram.get_account(self.username)

    def load_following(self):
        count_following = self.account.follows_count
        follow = self.instagram.get_following(self.account.identifier, count_following, 10, delayed=True)
        for f in follow["accounts"]:
            self.following.append(f.identifier)
            self.following_names.append(f.username)
        self.logger.log( "loaded {} followers ".format(len(self.following_names)))

    def is_user_following(self, user_id):
        """
        checks if user is following a given user

        :param user_id: user you want to check
        :return: True if following
        """
        return user_id in self.following

