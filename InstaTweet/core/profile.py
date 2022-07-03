from __future__ import annotations
import os
import pickle

from InstaTweet import db, utils
from InstaTweet.core import TweetClient


class Profile:
    LOCAL_DIR = os.path.join(utils.get_root(), 'profiles')

    def __init__(self, local=True, **kwargs):
        r"""Initialize a profile

        A :class:`Profile` contains a user map and all API access settings associated with it.
        Note that a name is not necessary to create and run a Profile, but it's required to save a Profile.

        :param local: if True, save files will be in the :attr:`~.LOCAL_DIR`. Otherwise, it will use a Postgres database
        :param kwargs: See :Keyword Arguments:

        * *name* (``str``) -- the profile name
             Unique identifier for a user map and associated Twitter/Instagram access keys
        * *session_id* (``str``) -- Instagram ``sessionid`` cookie
             Obtain by logging in through browser
        * *twitter_keys* (``dict``) -- Twitter API Keys with v1.1 endpoint access
            See :attr:`~TweetClient.DEFAULT_KEYS` for a template
        * *user_agent* (``str``) -- user agent for requests
             Will scrape for newest Chrome agent if not provided
        * *user_map* (``dict``) -- user map setup
            Fill this in later because blah blah writing words

        """
        self.name = kwargs.get('name', 'default')
        self.session_id = kwargs.get('session_id', '')
        self.twitter_keys = kwargs.get('twitter_keys', TweetClient.DEFAULT_KEYS)
        self.user_agent = kwargs.get('user_agent', utils.get_agent())
        self.user_map = kwargs.get('user_map', {})
        self.local = local

    @classmethod
    def load(cls, name: str, local: bool = True) -> Profile:
        """Loads an existing profile, either locally or from the database"""
        if not local:
            return db.load_profile(name)

        profile_path = cls.get_local_path(name)
        if os.path.exists(profile_path):
            with open(profile_path, 'rb') as f:
                return pickle.load(f)
        raise FileNotFoundError('No local profile found with that name')

    @staticmethod
    def get_local_path(name: str) -> str:
        """Returns filepath of where a local profile would be saved"""
        return utils.get_filepath(
            filename=os.path.join(Profile.LOCAL_DIR, name),
            filetype='pickle'
        )

    def save(self, name: str = None) -> bool:
        """Saves the current profile configuration using the current name or a new one

        :param name: name to save the profile under; will replace the current name
        """
        if name:
            self.name = name
        if self.is_default:  # Name not provided and not previously set
            raise AttributeError('Profile name is required to save the profile')

        return self._save_profile()

    def _save_profile(self):
        """Method is only called after profile is validated"""
        if not self.local:
            return db.save_profile(self)
        else:
            with open(self.profile_path, 'wb') as f:
                pickle.dump(self, f)
                print('Saved Profile ' + self.name)
        return True

    def to_pickle(self):
        return pickle.dumps(self)

    @property
    def is_default(self):
        """Check if default profile is being used. Used in initial save/load of profile"""
        return self.name == 'default'

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, isLocal: bool):
        if isLocal:
            if not os.path.exists(self.LOCAL_DIR):
                os.mkdir(self.LOCAL_DIR)
        self._local = isLocal

    @property
    def profile_path(self):
        if self.local and not self.is_default:
            return Profile.get_local_path(self.name)
