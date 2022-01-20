import os
import json
import copy
from collections.abc import Iterable

from InstaTweet.utils import UserAgent
from . import InstaClient, TweetClient

DEFAULT_USER_MAPPING = {'hashtags': [], 'scraped': [], 'tweets': []}
PACKAGE_DIR = os.path.dirname(__file__)


class InstaTweet:

    def __init__(self, **kwargs):
        self.profile_name = kwargs.pop('profile', 'default')
        self.session_id = kwargs.pop('session_id', '')
        self.user_agent = kwargs.pop('user_agent', UserAgent().default)
        self.twitter_keys = kwargs.pop('twitter_keys', None)
        self.user_map = kwargs.pop('user_map', {})

        if self.is_default:
            print('Using default profile.')
        else:
            self.load_profile(self.profile_name)

    @classmethod
    def load(cls, profile_name: str):
        return cls(profile=profile_name)

    def start(self):
        self.validate()
        insta = InstaClient(self.config)
        oauth = TweetClient.oauth(self.twitter_keys)

        for user, mapping in self.user_map.items():
            new_posts = insta.check_posts(user)
            if not new_posts:
                print(f'No new posts to tweet for @{user}')
                continue

            print(f'There are {len(new_posts)} posts to tweet for @{user}')
            for post in new_posts:
                insta.download_post(post, self.get_filepath(post.id))
                tweet = TweetClient(post, oauth, hashtags=mapping['hashtags'])
                tweet.send()

                mapping['scraped'] += [post.id]
                mapping['tweets'] += [post.tweet]

            print(f'Finished insta-tweeting for @' + user + '\n')

        print(f'All users have been insta-tweeted')
        if not self.is_default:
            self.save_profile()

    def add_users(self, users, scrape_only=True):
        """
        Add users to scrape and auto-tweet. Can be provided as a single username, an iterable containing usernames, or a full user_map dictionary.
        By default, new users will be scraped and any post after this point will be tweeted.
        Use scrape_only=False to immediately scrape AND tweet the user's most recent posts (12 by default).
        """
        user_map = self.user_map

        if isinstance(users, str):
            user_map.setdefault(users, copy.deepcopy(DEFAULT_USER_MAPPING))
            if not scrape_only:
            # Adding a fake post will cause tweets to be sent on the first scraoe
                user_map[users]['scraped'].append('-1')

        elif isinstance(users, Iterable):
            for user in users:
                self.add_users(user, scrape_only=scrape_only)

        elif isinstance(users, dict):
            for user in users:
                if users[user].get('hashtags') is None or users[user].get('scraped') is None:
                    raise AttributeError('Invalid user map structure')
            user_map.update(users)

        else:
            raise ValueError('Invalid type provided for parameter "users"')

        if not self.is_default:
            self.save_profile()

    def add_hashtags(self, user, hashtags):
        for hashtag in hashtags:
            if hashtag not in self.user_map[user]['hashtags']:
                self.user_map[user]['hashtags'].append(hashtag)

    def validate(self):
        if not self.session_id:
            raise AttributeError('Instagram sessionid cookie is required to scrape_only.')

        if missing_keys := [key for key in TweetClient.default_keys() if key not in self.twitter_keys]:
            raise KeyError(f'''
            Invalid Twitter API Keys Provided  
            Missing Keys: {missing_keys}''')

        if not all(self.twitter_keys.values()):
            twitter_file = self.get_filepath('Twitter API Keys')
            if not os.path.exists(twitter_file):
                raise ValueError(f'''
                Values missing for Twitter API Keys.
                Missing Values For: {[key for key, value in self.twitter_keys.items() if not value]}

                Default API Key file "{twitter_file}" is also missing.
                ''')

            try:
                # Setter will raise error if keys are invalid
                self.twitter_keys = self.load_data(twitter_file)
            except KeyError as e:
                raise e

        if not self.user_map:
            raise AttributeError('You must add at least one Instagram user to auto-tweet from')

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        """If an existing profile is currently loaded, it will be updated when setting a new session_id"""
        if not isinstance(session_id, str):
            raise ValueError('Session ID cookie must be of type str')
        self._session_id = session_id

        if session_id:
            if os.path.exists(self.get_filepath('profiles/' + self.profile_name)):
                self.save_profile()

    @property
    def twitter_keys(self):
        return self._twitter_keys

    @twitter_keys.setter
    def twitter_keys(self, keys: dict):
        default = TweetClient.default_keys()

        if isinstance(keys, dict):
            default.update(keys)
            if not all(default.values()):
                raise KeyError('No value provided for the following Twitter API Keys:' +
                               f'{[key for key in default if not default[key]]}')
            self._twitter_keys = keys

        elif keys is None:
            # Default init value
            self._twitter_keys = default

        else:
            raise TypeError(f'\n\n'
                            f'Twitter API Keys should be passed as a dictionary.\n'
                            f'See {self.get_filepath("Twitter API Keys")} for expected format\n'
                            f'Expected:\n'
                            f'{json.dumps(TweetClient.default_keys(), indent=4)}')

    def load_profile(self, profile_name: str):
        filepath = self.get_filepath('profiles/' + profile_name)

        if os.path.exists(filepath):
            profile = self.load_data(filepath)
            self._session_id = profile['session_id']
            self.user_agent = profile['user_agent']
            self.twitter_keys = profile['twitter_keys']
            self.user_map = profile['user_map']
            print(f'Loaded profile "{profile_name}"')

        else:
            new_profile = input(f'No profile found with the name {profile_name},'
                                f'would you like to create this profile? Y/N' + '\n' + '>> ')
            if new_profile.lower() == 'y':
                self.save_profile(profile_name)
            else:
                raise FileNotFoundError('No profile loaded')

    def save_profile(self, profile_name: str = None):
        """Update currently loaded profile, or save a new one. Name only required for new profiles."""
        if profile_name:
            self.profile_name = profile_name
        # Allows a loaded profile to be saved without specifying profile name
        if not self.is_default:
            self._save_data(self.config, 'profiles/' + self.profile_name)
            print(f'Saved profile "{self.profile_name}"')
        # If currently using default profile, must supply a profile name
        else:
            raise AttributeError('No profile currently loaded. Must provide a profile name')

    @property
    def is_default(self):
        return self.profile_name == 'default'

    @property
    def config(self):
        return {
            'session_id': self.session_id,
            'user_agent': self.user_agent,
            'twitter_keys': self.twitter_keys,
            'user_map': self.user_map
        }

    @staticmethod
    def get_filepath(filename):
        return os.path.join(PACKAGE_DIR, f'{filename}.txt')

    @staticmethod
    def load_data(filepath):
        with open(filepath, 'r') as data_in:
            return json.load(data_in)

    def _save_data(self, data, filename):
        filepath = self.get_filepath(filename)
        with open(filepath, 'w') as data_out:
            json.dump(data, data_out, indent=4)
