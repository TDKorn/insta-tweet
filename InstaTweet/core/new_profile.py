import os
import pickle
from InstaTweet import db, utils


class Profile:
    LOCAL_DIR = os.path.join(utils.get_root(), 'profiles')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'default')
        self.session_id = kwargs.get('session_id', '')
        self.twitter_keys = kwargs.get('twitter_keys', {})
        self.user_agent = kwargs.get('user_agent', utils.get_agent())
        self.user_map = kwargs.get('user_map', {})
        self.local = kwargs.get('local', False)

        if self.local:
            if not os.path.exists(self.LOCAL_DIR):
                os.mkdir(self.LOCAL_DIR)

    @classmethod
    def load(cls, name, local=True):
        """Loads an existing profile, either locally or from the database"""
        if not local:
            return db.load_profile(name)

        profile_path = cls.get_local_path(name)
        if os.path.exists(profile_path):
            with open(profile_path, 'rb') as f:
                return pickle.load(f)
        else:
            raise FileNotFoundError('No local profile found with that name')

    @staticmethod
    def get_local_path(name):
        """Returns filepath of where a local profile would be saved"""
        return utils.get_filepath(
            filename=os.path.join(Profile.LOCAL_DIR, name),
            filetype='pickle'
        )

    def save(self, name=None):
        """Validate and save profile configuration"""
        if name:
            self.name = name
        if not self.is_default:  # Either a name was provided, or a name was previously set
            return self._save_profile()
        else:  # No name provided and no name previously set; can't save
            raise AttributeError('Profile name is required to save the profile')

    def _save_profile(self):
        """Method is only called after profile is validated"""
        if not self.local:
            return db.save_profile(self)
        else:
            with open(self.profile_path, 'wb') as f:
                pickle.dump(self, f)
                print('Saved Profile ' + self.name)

    @property
    def is_default(self):
        """Check if default profile is being used. Used in initial save/load of profile"""
        return self.name == 'default'

    @property
    def profile_path(self):
        if self.local and not self.is_default:
            return Profile.get_local_path(self.name)

    def to_pickle(self):
        return pickle.dumps(self)
