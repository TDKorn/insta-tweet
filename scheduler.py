from InstaTweet import db

profiles = ['profile_1', 'profile_2']


def run(profile_name):
    it = db.load_profile(profile_name)
    it.start()


if __name__ == '__main__':
    for profile in profiles:
        run(profile)
