from __future__ import annotations

import os
import copy
import json
import pickle

from typing import Iterable
from . import utils, TweetClient, DBConnection, USER_AGENT


class Profile:

    USER_MAPPING = {'hashtags': [], 'scraped': [], 'tweets': []}
    LOCAL_DIR = os.path.join(utils.get_root(), 'profiles')

    def __init__(self, name: str = 'default', local: bool = True, **kwargs):
        """Create a new :class:`Profile`

        A :class:`Profile` contains a ``user_map`` and all API access settings associated with it

        ...

        The ``user_map`` is a mapping of added Instagram usernames to their associated :attr:`USER_MAPPING`

        * The mapping includes a list of hashtags, scraped posts, and sent tweets
        * Methods exist to access and modify these lists for a particular user
        * Mainly used to help compose tweets and detect when posts are new

        ...

        :param name: unique profile name
        :param local: indicates if profile is being saved locally or on a remote database
        :param kwargs: see below

        :Keyword Arguments:
            * *session_id* (``str``) --
                Instagram ``sessionid`` cookie, obtained by logging in through browser
            * *twitter_keys* (``dict``) --
                Twitter API Keys with v1.1 endpoint access
                * See :attr:`~InstaTweet.tweetclient.TweetClient.DEFAULT_KEYS` for a template
            * *user_agent* (``str``) -- Optional
                The user agent to use for requests; uses a currently working hardcoded agent if not provided
            * *proxy_key* (``str``) -- Optional
                Name of environment variable to retrieve proxies from
            * *user_map* (``dict``) -- Optional
                A dict of Instagram users and their associated :attr:`~.USER_MAPPING`

        :Note:
            A name is not necessary to create and *InstaTweet* a profile, but it's required to :meth:`~.save` it

        """
        self.local = local
        self.name = name    # Will raise Exception if name is already used

        self.session_id = kwargs.get('session_id', '')
        self.twitter_keys = kwargs.get('twitter_keys', TweetClient.DEFAULT_KEYS)
        self.user_agent = kwargs.get('user_agent', USER_AGENT)
        self.proxy_key = kwargs.get('proxy_key', None)
        self.user_map = kwargs.get('user_map', {})

    @classmethod
    def load(cls, name: str, local: bool = True) -> Profile:
        """Loads an existing profile from a locally saved pickle file or remotely stored pickle byte string

        :param name: the name of the :class:`Profile` to load
        :param local: whether the profile is saved locally (default, ``True``) or remotely on a database
            If saved remotely, the ``DATABASE_URL`` environment variable must be configured
        """
        if not cls.profile_exists(name, local):
            raise LookupError(
                f'No {"local" if local else "database"} profile found with the name "{name}"'
            )
        if local:
            with open(cls.get_local_path(name), 'rb') as f:
                return pickle.load(f)
        else:
            with DBConnection() as db:
                return db.load_profile(name)

    @classmethod
    def from_json(cls, json_str: str) -> Profile:
        """Creates a profile from a JSON formatted string of config settings"""
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, d: dict) -> Profile:
        """Creates a profile from a dictionary of config settings"""
        return cls(**d)

    @staticmethod
    def profile_exists(name: str, local: bool = True) -> bool:
        """Check if a profile with the given name and location (local/remote) already exists"""
        if local:
            return os.path.exists(Profile.get_local_path(name))
        else:
            with DBConnection() as db:
                return bool(db.query_profile(name).first())

    @staticmethod
    def get_local_path(name: str) -> str:
        """Returns filepath of where a local profile would be saved"""
        return os.path.join(Profile.LOCAL_DIR, name) + '.pickle'

    def add_users(self, users: Iterable, send_tweet: bool = False):
        """Add Instagram user(s) to the :attr:`~.user_map` for subsequent monitoring

        By default, newly added users will not have their posts tweeted the first time they are scraped -
        the IDs of their recent posts are stored, and any new posts from that point forward will be tweeted

        You can override this by setting ``send_tweet=True``, which will immediately scrape AND tweet the recent posts

        :param users: Instagram username(s) to automatically scrape and tweet content from
        :param send_tweet: choose if tweets should be sent on the first scrape, or only for new posts going forward
        """
        if not isinstance(users, Iterable):
            raise TypeError(f'Invalid type provided. `users` must be an Iterable')
        if isinstance(users, str):
            users = [users]

        for user in users:
            mapping = copy.deepcopy(Profile.USER_MAPPING)
            self.user_map.setdefault(user, mapping)

            if send_tweet:  # Non-empty scraped list will trigger Tweets to send
                self.get_scraped_from(user).append(-1)

            print(f'Added Instagram user @{user} to the user map')

        if self.exists:
            self._save_profile(alert=False)

    def add_hashtags(self, user: str, hashtags: Iterable):
        """Add hashtag(s) to a user in the :attr:`~.user_map`, which will be randomly chosen from when composing Tweets

        :param user: the user in the user map to add hashtags to
        :param hashtags: hashtags to choose from and include in any Tweets where content comes from this user
        """
        if not isinstance(hashtags, Iterable):
            raise TypeError("Hashtags must be provided as a string or iterable of strings")
        if isinstance(hashtags, str):
            hashtags = [hashtags]

        tags = self.get_hashtags_for(user)  # Retrieve the current hashtag list
        tags.extend(set(hashtags) - set(tags))  # Add new ones (case-sensitive)

        if self.exists:
            self._save_profile(alert=False)
        print(f'Added hashtags for @{user}')

    def save(self, name: str = None, alert: bool = True) -> bool:
        """Pickles and saves the :class:`Profile` using the specified or currently set name.

        :param name: name to save the :class:`Profile` under; replaces the current :attr:`~.name`
        :param alert: set to ``True`` to print a message upon successful save
        """
        if name:
            self.name = name
        if self.is_default:  # Profile name wasn't specified and wasn't previously set
            raise AttributeError('Profile name is required to save the profile')
        else:
            return self._save_profile(alert=alert)

    def _save_profile(self, alert: bool = True) -> bool:
        """Internal function to save the profile, based on the value of :attr:`~.local`"""
        if self.local:
            with open(self.profile_path, 'wb') as f:
                pickle.dump(self, f)
            if alert:
                print(f'Saved Local Profile {self.name}')
            return True
        else:
            with DBConnection() as db:
                return db.save_profile(profile=self, alert=alert)

    def validate(self) -> None:
        """Checks to see if the Profile is fully configured for InstaTweeting

        :raises ValueError: if the :attr:`~.session_id`, :attr:`~.twitter_keys`, or :attr:`~.user_map` are invalid
        """
        if not self.session_id:
            raise ValueError('Instagram sessionid cookie is required to scrape posts')

        if bad_keys := [key for key, value in self.twitter_keys.items() if value == 'string']:
            raise ValueError(f'Values not set for the following Twitter keys: {bad_keys}')

        if not self.user_map:
            raise ValueError('You must add at least one Instagram user to auto-tweet from')

    def to_pickle(self) -> bytes:
        """Serializes profile to a pickled byte string"""
        return pickle.dumps(self)

    def to_json(self) -> str:
        """Serializes profile to a JSON formatted string"""
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:
        """Serializes profile to a dict"""
        return self.config

    def view_config(self):
        """Prints the :attr:`~.config` dict to make it legible"""
        for k, v in self.config.items():
            print(f'{k} : {v}')

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

    def get_user(self, user: str) -> dict:
        """Returns the specified user's dict entry in the :attr:`user_map`"""
        return self.user_map[user]

    def get_scraped_from(self, user: str) -> list:
        """Returns a list of posts that have been scraped from the specified user"""
        return self.user_map[user]['scraped']

    def get_tweets_for(self, user: str) -> list:
        """Returns a list of tweets that use the specified user's scraped content"""
        return self.user_map[user]['tweets']

    def get_hashtags_for(self, user: str) -> list:
        """Returns the hashtag list for the specified user"""
        return self.user_map[user]['hashtags']

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
        """Instagram ``sessionid`` cookie, obtained by logging in through a browser

            :Tip: If you log into your account with a browser you don't use, the session cookie will last longer
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        if not isinstance(session_id, str):
            raise TypeError(
                f'Session ID cookie must be of type {str}'
            )
        self._session_id = session_id
        if self.exists:
            self._save_profile(alert=False)

    @property
    def twitter_keys(self) -> dict:
        """Twitter developer API keys with v1.1 endpoint access. See :attr:`~.DEFAULT_KEYS`"""
        return self._twitter_keys

    @twitter_keys.setter
    def twitter_keys(self, api_keys: dict):
        if not isinstance(api_keys, dict):
            raise TypeError(
                f'Twitter Keys must be of type {dict}'
            )
        if missing_keys := [key for key in TweetClient.DEFAULT_KEYS if key not in api_keys]:
            raise KeyError(
                f'Missing Twitter Keys: {missing_keys}'
            )
        for key in TweetClient.DEFAULT_KEYS:
            if not bool(api_keys[key]):
                raise ValueError(
                    f'Missing Value for Twitter Key: {key}'
                )
        self._twitter_keys = api_keys
        if self.exists:
            self._save_profile(alert=False)
