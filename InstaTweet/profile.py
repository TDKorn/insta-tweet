from __future__ import annotations

import os
import copy
import json
import pickle

from typing import Iterable
from . import TweetClient, DBConnection, USER_AGENT


class Profile:

    """The :class:`Profile` is a configuration class used extensively throughout the package

    It consists of a :attr:`~user_map` and an associated collection of API/web scraping :ref:`settings <settings>`

    ...

    .. admonition:: About the User Map
        :class: instatweet

        The :attr:`~user_map` is a dict containing info about the users added to a :class:`Profile`

        * It's used to help detect new posts and compose tweets on a per-user basis
        * Entries are created when you :meth:`add_users`, which map the user to a :attr:`~USER_MAPPING`
        * The :attr:`~USER_MAPPING` maintains lists of hashtags, scraped posts, and sent tweets
        * The mapping is updated when you :meth:`add_hashtags` and successfully :meth:`~.send_tweet`

        You can access entries in the :attr:`~user_map` as follows:

        * :meth:`~get_user` allows you to retrieve a full entry by username
        * :meth:`~get_hashtags_for`, :meth:`get_scraped_from`, :meth:`get_tweets_for` provide access
          to lists

    ...

    **[Optional]**

    A unique, identifying :attr:`~name` can be assigned to the Profile, which
    may then be used to :meth:`~save` and, in turn, :meth:`~load` its settings

    * This makes it extremely easy to switch between Profiles and create templates

    Saving isn't a requirement to :meth:`~.start` InstaTweet, but...

    * To :meth:`~.get_new_posts`, InstaTweet makes comparisons
      with the ``scraped`` list in the :attr:`~.user_map`
    * Saving this list ensures you don't :meth:`~.send_tweet`
      for a post more than once

    ...

    .. admonition:: Important
       :class: important-af

       If you do :meth:`~save` your profile, the save location is determined by the value of :attr:`Profile.local`

       * Local saves are made to the :attr:`~LOCAL_DIR`, as pickle files
       * Remote saves are made to a database (via the :mod:`~.db` module) as pickle bytes

       **You MUST configure the** :attr:`~InstaTweet.db.DATABASE_URL` **environment variable to save/load remotely**

       * InstaTweet uses ``SQLAlchemy`` to create a :class:`~.DBConnection` -- any db it supports is compatible
       * See the :mod:`~.db` module for more information

    """

    USER_MAPPING = {'hashtags': [], 'scraped': [], 'tweets': []}  #: Template for an entry in the ``user_map``
    LOCAL_DIR = os.path.abspath('profiles')  #: Directory where local profiles are saved

    def __init__(self, name: str = 'default', local: bool = True, **kwargs):
        """Create a new :class:`Profile`

        .. note:: :class:`Profile` creation is mandatory to use the ``InstaTweet`` package

           * Required as a parameter to initialize an :class:`~.InstaTweet` object
           * Naming and saving it is ideal, but not necessary to :meth:`~.start` InstaTweet

        :param name: unique profile name
        :param local: indicates if profile is being saved locally or on a remote database
        :param kwargs: see below

        :Keyword Arguments:
            * *session_id* (``str``)
                Instagram ``sessionid`` cookie, obtained by logging in through browser
            * *twitter_keys* (``dict``)
                Twitter API Keys with v1.1 endpoint access
                (see :attr:`~.TweetClient.DEFAULT_KEYS` for a template)
            * *user_agent* (``str``) -- Optional
                The user agent to use for requests; uses a currently working hardcoded agent if not provided
            * *proxy_key* (``str``) -- Optional
                Environment variable to retrieve proxies from
            * .. autoattribute:: user_map
                 :annotation:
                 :noindex:

        .. admonition:: **Profile Creation Tips**
           :class: instatweet

           * All attributes can be passed as arguments at initialization or set directly afterwards
           * Property setters validate data types for the :ref:`mandatory-settings`
           * The :class:`~Profile` as a whole is validated by :meth:`~validate`


        """
        self.local = local
        self.name = name    # Will raise Exception if name is already used

        self.session_id = kwargs.get('session_id', '')
        self.twitter_keys = kwargs.get('twitter_keys', TweetClient.DEFAULT_KEYS)
        self.user_agent = kwargs.get('user_agent', USER_AGENT)
        self.proxy_key = kwargs.get('proxy_key', None)
        self.user_map = kwargs.get('user_map', {})  #: ``dict``: Mapping of added Instagram users and their :attr:`~USER_MAPPING`

    @classmethod
    def load(cls, name: str, local: bool = True) -> Profile:
        """Loads an existing profile from a locally saved pickle file or remotely stored pickle bytes

        :param name: the name of the :class:`Profile` to load
        :param local: whether the profile is saved locally (default, ``True``) or remotely on a database

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
        """Checks locally/remotely to see if a :class:`~Profile` with the specified name has an existing save file

        Whenever the :attr:`~name` is changed, its property setter calls this method to ensure
        you don't accidentally overwrite a save that already :attr:`~exists`

        :param name: the name of the :class:`Profile` to check for
        :param local: the location (local/remote) to check for an existing save

        """
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

        .. note:: By default, newly added users won't have their posts tweeted the first time they're scraped

           * The IDs of the ~12 most recent posts are stored in the ``scraped`` list
           * Any new posts from that point forward will be tweeted

           You can override this by setting ``send_tweet=True``

           * This causes their ~12 most recent posts to be scraped AND tweeted

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
        """Indicates if saves should be made locally (``True``) or on a remote database (``False``)

         :rtype: bool
         """
        return self._local

    @local.setter
    def local(self, local: bool):
        if local:
            if not os.path.exists(self.LOCAL_DIR):
                os.mkdir(self.LOCAL_DIR)

        self._local = local

    @property
    def name(self) -> str:
        """A name for the Profile

        The :attr:`~Profile.name` is used differently depending on the value of :attr:`~.local`

        * ``local==True``: the name determines the :attr:`~.profile_path` (path where it would save to)
        * ``local==False``: the name is used as the primary key in the :class:`~.Profiles` database table

        ...

        .. admonition:: Profile Names Must Be Unique
            :class: instatweet

            When you set or change the :attr:`~.name`, a property setter will make sure no
            :meth:`~profile_exists` with that name before actually updating it

            * This ensures that you don't accidentally overwrite a different Profile's save data

        ...

        :raises FileExistsError: if :attr:`~local` ``==True`` and a save is found in the :attr:`~LOCAL_DIR`
        :raises ResourceWarning: if :attr:`~local` ``==False`` and a database row is found by :meth:`~.db.query_profile`
        """
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
