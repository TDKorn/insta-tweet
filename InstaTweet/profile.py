from __future__ import annotations

import os
import copy
import pickle

from typing import Iterable
from . import utils, TweetClient


class Profile:

    USER_MAPPING = {'hashtags': [], 'scraped': [], 'tweets': []}
    LOCAL_DIR = os.path.join(utils.get_root(), 'profiles')

    def __init__(self, name: str = 'default', local: bool = True, **kwargs):
        """Initialize a profile

        A :class:`Profile` contains a user map and all API access settings associated with it.
        Note that a name is not necessary to create and run a Profile, but it's required to save a Profile.

        :param name: profile name; unique identifier for a user map and its associated Twitter/Instagram access keys
        :param local: if True, pickle files will save to the :attr:`~.LOCAL_DIR`. Otherwise, will save to a Postgres DB
        :param kwargs: see below

        :Keyword Arguments:
            * *session_id* (``str``) --
              Instagram ``sessionid`` cookie, obtained by logging in through browser
            * *twitter_keys* (``dict``) --
              Twitter API Keys with v1.1 endpoint access
                * See :attr:`~TweetClient.DEFAULT_KEYS` for a template
            * *user_agent* (``str``) --
              user agent to use for requests. Will scrape newest Chrome agent if not provided
            * *user_map* (``dict``) --
              Fill this in later because blah blah writing words
        """
        self.local = local
        self.name = name    # Will raise Exception if name is already used

        self.session_id = kwargs.get('session_id', '')
        self.twitter_keys = kwargs.get('twitter_keys', TweetClient.DEFAULT_KEYS)
        self.user_agent = kwargs.get('user_agent', utils.get_agent())
        self.proxy_key = kwargs.get('proxy_key', None)
        self.user_map = kwargs.get('user_map', {})

    @classmethod
    def load(cls, name: str, local: bool = True) -> Profile:
        """Loads an existing profile, either locally or from the database

        :param name: the name of the :class:`Profile` to load
        :param local: whether the profile is saved locally (default, True) or remotely on a database
            If saved remotely, the ``DATABASE_URL`` environment variable must be configured
        """
        if local:
            if Profile.profile_exists(name):
                with open(Profile.get_local_path(name), 'rb') as f:
                    return pickle.load(f)
            else:
                raise FileNotFoundError('No local profile found with that name')

        from InstaTweet.db import load_profile
        return load_profile(name)

    @staticmethod
    def profile_exists(name: str, local: bool = True) -> bool:
        """Check if a profile with the given name and location (local/remote) already exists"""
        if local:
            return os.path.exists(Profile.get_local_path(name))
        else:
            from InstaTweet.db import query_profile
            return bool(query_profile(name).first())

    @staticmethod
    def get_local_path(name: str) -> str:
        """Returns filepath of where a local profile would be saved"""
        return utils.get_filepath(
            filename=os.path.join(Profile.LOCAL_DIR, name),
            filetype='pickle'
        )

    def add_users(self, users: Iterable, send_tweet: bool = False):
        """Add multiple Instagram user(s) to the :attr:`~.user_map` for subsequent monitoring

        :param users: an iterable of Instagram usernames to automatically scrape and tweet content from
        :param send_tweet: indicate if tweets should be sent on the first scrape or only for new posts going forward
        """
        if not isinstance(users, Iterable):
            raise TypeError(f'Invalid type provided. `users` must be an Iterable')
        if isinstance(users, str):
            users = [users]

        for user in users:
            self.add_user(user, send_tweet)

    def add_user(self, user: str, send_tweet: bool = False):
        """Add a single Instagram user to the :attr:`~.user_map` for subsequent monitoring

        By default, newly added users will not have their posts tweeted the first time they are scraped - the post IDs
        of the most recent 12 posts are stored, and any new posts from this point forward will be tweeted
        You can override this by setting ``send_tweet=True``, which immediately scrapes AND tweets the most recent posts

        :param user: the Instagram username to add (without the "@")
        :param send_tweet: indicate if tweets should be sent on the first scrape or only for new posts going forward
        """
        self.user_map.setdefault(user, copy.deepcopy(self.USER_MAPPING))

        if send_tweet:
            self.user_map[user]['scraped'].append('-1')
        if self.exists:
            self._save_profile(alert=False)

        print(f'Added Instagram user @{user} to the user map')

    def add_hashtags(self, user: str, hashtags: Iterable):
        """Add hashtag(s) to a user in the :attr:`~.user_map`, which will be randomly chosen from when composing Tweets

        :param user: the user in the user map to add hashtags to
        :param hashtags: hashtags to choose from and include in any Tweets where content comes from this user
        """
        if not isinstance(hashtags, Iterable):
            raise TypeError("Hashtags must be provided as a string or iterable of strings")
        if isinstance(hashtags, str):
            hashtags = [hashtags]

        tags = self.user_map[user]['hashtags']
        for hashtag in hashtags:
            if hashtag not in tags:
                tags.append(hashtag)

        if self.exists:
            self._save_profile(alert=False)
        print(f'Added hashtags for @{user}')

    def validate(self) -> None:
        """Checks to see if the profile is fully configured for InstaTweeting

        :raises ValueError: if the :attr:`~.session_id`, :attr:`~.twitter_keys`, or :attr:`~.user_map` are invalid
        """
        if not self.session_id:
            raise ValueError('Instagram sessionid cookie is required to scrape posts')

        if bad_keys := [key for key, value in self.twitter_keys.items() if value == 'string']:
            raise ValueError(f'Values not set for the following Twitter keys: {bad_keys}')

        if not self.user_map:
            raise ValueError('You must add at least one Instagram user to auto-tweet from')

    def save(self, name: str = None, alert: bool = True) -> bool:
        """Saves the Profile as a pickled object, using the specified or currently set name.

        :param name: name to save the profile under; replaces the current name
        :param alert: set to ``True`` to print a message upon successful save
        """
        if name:
            self.name = name
        if not self.is_default:
            return self._save_profile(alert=alert)
        else:  # Profile name wasn't specified and wasn't previously set
            raise AttributeError('Profile name is required to save the profile')

    def _save_profile(self, alert: bool = True) -> bool:
        """Internal function to save the profile, based on the value of :attr:`~.local`"""
        if self.local:
            with open(self.profile_path, 'wb') as f:
                pickle.dump(self, f)
            if alert:
                print(f'Saved Local Profile {self.name}')
            return True
        else:
            from InstaTweet.db import save_profile
            return save_profile(profile=self, alert=alert)

    def view_config(self):
        """Prints the :attr:`~.config` dict to make it legible"""
        for k, v in self.config.items():
            print(f'{k} : {v}')

    def to_pickle(self) -> bytes:
        return pickle.dumps(self)

    @property
    def exists(self) -> bool:
        """Returns True if a local save file or database record exists for the currently set profile name"""
        return self.profile_exists(name=self.name, local=self.local)

    @property
    def is_default(self) -> bool:
        """Check if profile :attr:`~.name` is set or not"""
        return self.name == 'default'

    @property
    def profile_path(self) -> str:
        """If :attr:`~.local` is ``True``, returns the file path for where this profile would be/is saved"""
        if self.local and not self.is_default:
            return Profile.get_local_path(self.name)
        return ''

    @property
    def local(self) -> bool:
        """Indicates if profile is being saved locally (``True``) or on a remote database (``False``)"""
        return self._local

    @local.setter
    def local(self, local: bool):
        if local:
            if not os.path.exists(self.LOCAL_DIR):
                os.mkdir(self.LOCAL_DIR)

        self._local = local

    @property
    def name(self) -> str:
        """The profile name"""
        return self._name

    @name.setter
    def name(self, profile_name):
        """Sets the profile name, if a profile with that name doesn't already exist locally/remotely"""
        if profile_name != 'default' and self.profile_exists(profile_name, local=self.local):
            if self.local:
                raise FileExistsError(
                    'Local save file already exists for profile named "{}"\n'.format(profile_name) +
                    'Please choose another name, load the profile, or delete the file.')
            else:
                raise ResourceWarning(
                    'Database record already exists for profile named "{}"\n'.format(profile_name) +
                    'Please choose another name or use InstaTweet.db to load/delete the profile'
                )
        self._name = profile_name

    @property
    def session_id(self) -> str:
        """The Instagram ``sessionid`` cookie"""
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        if not isinstance(session_id, str):
            raise TypeError('Session ID cookie must be of type str')
        self._session_id = session_id

        if self.exists:
            self._save_profile(alert=False)

    @property
    def twitter_keys(self) -> dict:
        """The Twitter developer API keys with v1.1 endpoint access"""
        return self._twitter_keys

    @twitter_keys.setter
    def twitter_keys(self, twitter_api_keys: dict):
        if not isinstance(twitter_api_keys, dict):
            raise TypeError(f'Twitter Keys must be type {dict}')

        if missing_keys := [key for key in TweetClient.DEFAULT_KEYS if key not in twitter_api_keys]:
            raise KeyError(f'Missing Twitter Keys: {missing_keys}')

        for key in TweetClient.DEFAULT_KEYS:
            if not bool(twitter_api_keys[key]):
                raise ValueError(f'Missing Value for Twitter Key: {key}')

        self._twitter_keys = twitter_api_keys

        if self.exists:
            self._save_profile(alert=False)

    @property
    def config(self) -> dict:
        """Returns a dictionary containing important configuration settings"""
        return {
            'name': self.name,
            'local': self.local,
            'session_id': self.session_id,
            'twitter_keys': self.twitter_keys,
            'user_agent': self.user_agent,
            'proxy_key': self.proxy_key,
            'user_map': self.user_map,
        }
