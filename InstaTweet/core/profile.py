from __future__ import annotations

import copy
import os
import pickle
from typing import Union, Iterable

from InstaTweet import db, utils
from InstaTweet.core import TweetClient, InstaClient


class Profile:
    LOCAL_DIR = os.path.join(utils.get_root(), 'profiles')
    USER_MAPPING = {'hashtags': [], 'scraped': [], 'tweets': []}

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
        self.local = local
        self.name = kwargs.get('name', 'default')

        if self.exists:
            raise FileExistsError("Profile with that name already exists. Please use Profile.load('name')")

        self.session_id = kwargs.get('session_id', '')
        self.twitter_keys = kwargs.get('twitter_keys', TweetClient.DEFAULT_KEYS)
        self.user_agent = kwargs.get('user_agent', utils.get_agent())
        self.user_map = kwargs.get('user_map', {})

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

    def _save_profile(self, alert=True):
        """Method is only called after profile is validated"""
        if not self.local:
            return db.save_profile(self, alert=alert)
        else:
            with open(self.profile_path, 'wb') as f:
                pickle.dump(self, f)

        if alert:
            print('Saved Profile ' + self.name)
        return True

    def to_pickle(self):
        return pickle.dumps(self)

    @property
    def exists(self):
        """Returns True if a local save file or database record exists for the profile name"""
        if self.local:
            return os.path.exists(self.profile_path)
        return bool(db.query_profile(self.name).first())

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
        return ''

    def add_user(self, user: str, send_tweet: bool = False):
        self.user_map.setdefault(user, copy.deepcopy(self.USER_MAPPING))
        if send_tweet:
            # Tweets are, by default sent only when posts have previously been scraped
            self.user_map[user]['scraped'].append('-1')

        print(f'Added {user} to the user map')
        if not self.is_default:
            return self._save_profile(alert=False)

    def add_users(self, users: Iterable, send_tweet: bool = False):
        """Add Instagram user(s) to monitor for new posts to scrape and tweet.

        By default, new users will be scraped and any post after this point will be tweeted.
        Set ``send_tweet=True`` to immediately scrape AND tweet the user's most recent 12 posts

        :param users: Instagram user(s) to automatically tweet content from
        :param send_tweet: choose if tweets should be sent on the first scrape or for posts going forward
        """
        if not isinstance(users, Iterable):
            raise TypeError(f'Invalid type provided. `users` must be an Iterable')

        for user in users:
            self.add_user(user, send_tweet=send_tweet)
