from InstaTweet import InstaTweet

PROFILES = ['aProfile', 'myProfile']
LOCAL = True


def run(profile_name: str, local: bool = LOCAL):
    """Loads and InstaTweets a profile

    :param profile_name: the name of the :class:`~.Profile`
    :param local: if the profile is saved locally or in a SQLAlchemy supported database
    """
    insta_tweet = InstaTweet.load(profile_name, local=local)
    insta_tweet.start()


if __name__ == '__main__':
    for profile in PROFILES:
        run(profile, local=LOCAL)
