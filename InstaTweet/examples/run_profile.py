from InstaTweet import InstaTweet

profiles = ['profile1']


def run(profile_name):
    """Use this to run fully configured profiles"""
    it = InstaTweet.load(profile_name)
    it.start()


if __name__ == '__main__':
    for profile in profiles:
        run(profile)
