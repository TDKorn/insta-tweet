import pickle
from InstaTweet import db
from InstaTweet.utils import *
from abc import ABC, abstractmethod


class Profile(ABC):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'default')
        self.session_id = kwargs.get('session_id', '')
        self.twitter_keys = kwargs.get('twitter_keys', {})
        self.user_agent = kwargs.get('user_agent', get_agent())
        self.user_map = kwargs.get('user_map', {})

    @classmethod
    @abstractmethod
    def load(cls, name):
        """Load an existing profile"""
        pass

    def save(self, name=None):
        """Validate profile name and save configuration"""
        if name:
            self.name = name
        else:
            if self.is_default:
                raise AttributeError('Profile name is required')

        self.save_profile()

    @abstractmethod
    def save_profile(self):
        """Method is only called after profile is validated"""
        pass

    @property
    def is_default(self):
        """Check if default profile is being used. Used in initial save/load of profile"""
        return self.name == 'default'


class DBProfile(Profile):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def load(cls, name):
        return db.load_profile(name)

    def save_profile(self):
        db.save_profile(self)

    def to_pickle(self):
        return pickle.dumps(self)


class LocalProfile(Profile):
    PROFILE_DIR = os.path.join(get_root(), 'profiles')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not os.path.exists(self.PROFILE_DIR):
            os.mkdir(self.PROFILE_DIR)

    @classmethod
    def load(cls, name):
        fp = cls.get_profile_path(name)
        if os.path.exists(fp):
            with open(fp, 'rb') as f:
                return pickle.load(f)
        else:
            raise FileNotFoundError('No profile found with that name')

    def save_profile(self):
        with open(self.profile_path, 'wb') as f:
            pickle.dump(self, f)
            print('Saved Profile ' + self.name)

    @property
    def profile_path(self):
        return self.get_profile_path(self.name)

    @staticmethod
    def get_profile_path(name):
        if name == 'default':
            return ''
        return get_filepath(os.path.join(LocalProfile.PROFILE_DIR, name), filetype='pickle')
