from __future__ import annotations

import copy
import os
import pickle

from typing import Iterable
from . import db, utils, TweetClient


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
        self.user_map = kwargs.get('user_map', {})

    @classmethod
    def load(cls, name: str, local: bool = True) -> Profile:
        """Loads an existing profile, either locally or from the database"""
        if not local:
            return db.load_profile(name)

        if cls.profile_exists(name):
            with open(cls.get_local_path(name), 'rb') as f:
                return pickle.load(f)

        raise FileNotFoundError('No local profile found with that name')

    @staticmethod
    def get_local_path(name: str) -> str:
        """Returns filepath of where a local profile would be saved"""
        return utils.get_filepath(
            filename=os.path.join(Profile.LOCAL_DIR, name),
            filetype='pickle'
        )

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
        if not self.local:
            return db.save_profile(self, alert=alert)
        else:
            with open(self.profile_path, 'wb') as f:
                pickle.dump(self, f)
        if alert:
            print(f'Saved Local Profile {self.name}')
        return True

    def add_users(self, users: Iterable, send_tweet: bool = False):
        """Add multiple Instagram user(s) to the :ivar:`~.user_map` for subsequent monitoring

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
        """Add a single Instagram user to the :ivar:`~.user_map` for subsequent monitoring

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
        """Add hashtag(s) to a user in the :ivar:`user_map`, which will be randomly chosen from when composing Tweets

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

    def to_pickle(self):
        return pickle.dumps(self)

    def view_config(self):
        """:meth:`~.config` but make it legible ♥"""
        for k, v in self.config.items():
            print(f'{k} : {v}')

    @staticmethod
    def profile_exists(name: str, local: bool = True) -> bool:
        """Check if a profile with the given name and location (local/remote) already exists"""
        if local:
            return os.path.exists(Profile.get_local_path(name))
        else:
            return bool(db.query_profile(name).first())

    @property
    def exists(self) -> bool:
        """Returns True if a local save file or database record exists for the currently set profile name"""
        return self.profile_exists(name=self.name, local=self.local)

    @property
    def is_default(self):
        """Check if default profile is being used. Used in initial save/load of profile"""
        return self.name == 'default'

    @property
    def profile_path(self):
        if self.local and not self.is_default:
            return Profile.get_local_path(self.name)
        return ''

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
    def name(self):
        return self._name

    @name.setter
    def name(self, profile_name):
        """Sets the profile name, if a profile with that name doesn't already exist locally/remotely"""
        if profile_name != 'default' and self.profile_exists(profile_name, local=self.local):
            if self.local:
                raise FileExistsError(
                    f'Local save file with the name "{profile_name}" already exists. Please choose another name, '
                    'load the profile, or delete the file.'
                )
            else:
                raise ResourceWarning(
                    f'Database record already exists for profile named "{profile_name}" already exists.' + '\n' +
                    'Please choose another name or use InstaTweet.db load/delete the profile'
                )
        self._name = profile_name

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        if not isinstance(session_id, str):
            raise TypeError('Session ID cookie must be of type str')
        self._session_id = session_id

        if self.exists:
            self._save_profile(alert=False)

    @property
    def twitter_keys(self):
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
    def config(self):
        return {
            'name': self.name,
            'local': self.local,
            'session_id': self.session_id,
            'user_agent': self.user_agent,
            'twitter_keys': self.twitter_keys,
            'user_map': self.user_map,
        }

    def validate(self) -> bool:
        """Checks to see if the profile is fully configured

            :NOTE:
                Property setters do the actual data validation
        """
        if not self.session_id:
            raise ValueError('Instagram sessionid cookie is required to scrape posts')

        if bad_keys := [key for key, value in self.twitter_keys.items() if value == 'string']:
            raise ValueError(
                'Using default values for the following Twitter keys:\n{}'.format(bad_keys)
            )
        if not self.user_map:
            raise ValueError('You must add at least one Instagram user to auto-tweet from')

        return True
