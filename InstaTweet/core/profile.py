import os
import pickle

from InstaTweet.utils import *

DB = 0
LOCAL = 1
PROFILE_DIR = os.path.join(get_root(), 'profiles')


class Profile:

    def __init__(self, type, **kwargs):
        if type in [DB, LOCAL]:
            self.type = type
        else:
            raise AttributeError('Invalid profile type. Must be Profile.DB or Profile.LOCAL')

        self.name = kwargs.get('name', 'default')
        self.session_id = kwargs.get('session_id', '')
        self.twitter_keys = kwargs.get('twitter_keys', {})
        self.user_agent = kwargs.get('user_agent', get_agent())
        self.user_map = kwargs.get('user_map', {})

        if not os.path.exists(PROFILE_DIR):
            os.mkdir(PROFILE_DIR)

    def save(self, name=None):
        if name:
            self.name = name
        else:
            if self.is_default:
                raise AttributeError('Profile name is required')

        if self.type == DB:
            pass

        elif self.type == LOCAL:
            save_local(self)

    @classmethod
    def load(cls, name, type):
        if type == DB:
            pass
        elif type == LOCAL:
            return load_local(name)
        else:
            raise TypeError('Invalid profile type. Must be Profile.DB or Profile.LOCAL')

    @property
    def is_default(self):
        """Check if default profile is being used. Used in initial save/load of profile"""
        return self.name == 'default'

    @property
    def profile_path(self):
        return get_profile_path(self.name)


def get_profile_path(name):
    return get_filepath(os.path.join(PROFILE_DIR, name), filetype='pickle')


def save_local(profile: Profile):
    with open(profile.profile_path, 'wb') as f:
        pickle.dump(profile, f)


def load_local(name):
    fp = get_profile_path(name)
    with open(fp, 'rb') as f:
        return pickle.load(f)
