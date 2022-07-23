from __future__ import annotations
import os
import pickle
import InstaTweet

from sqlalchemy import create_engine, Column, String, LargeBinary
from sqlalchemy.orm import sessionmaker, scoped_session, Query
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = os.getenv('DATABASE_URL', '').replace('postgres://', 'postgresql://', 1)
"""The Database URL to use, obtained from the ``DATABASE_URL`` environment variable"""

Base = declarative_base()
"""Base for creating tables"""


class Profiles(Base):
    """Database table used for storing :class:`~.Profile` settings

    The table currently has only 2 fields, for the :attr:`~.Profile.name` and pickle bytes of the profile
    """
    __tablename__ = 'profiles'
    name = Column(String, primary_key=True)  #: The :class:`~.Profile` name
    config = Column(LargeBinary)  #: The pickle bytes from :meth:`.Profile.to_pickle()`

    def __repr__(self):
        return "<Profiles(name='{}')>".format(self.name)


class DBConnection:

    """Database Connection class with context management ooh wow

    Uses ``SQLAlchemy`` to connect and interact with the database specified by :attr:`DATABASE_URL` environment variable

    **Sample Usage**::

        def poop_check():
            with DBConnection() as db:
                if db.query_profile(name="POOP").first():
                    raise FileExistsError('DELETE THIS NEPHEW......')
    """

    SESSION = None
    """The currently active session; closed on object exit
    
    :type: :class:`~.sqlalchemy.orm.scoping.scoped_session`
    """

    ENGINE = None
    """The engine for the currently set :attr:`DATABASE_URL`; reused after first connection
    
    :type: :class:`~.sqlalchemy.engine.base.Engine`
    """

    def __enter__(self):
        if not DATABASE_URL:
            raise EnvironmentError('Must set the DATABASE_URL environment variable')

        if not self.ENGINE:
            engine = create_engine(DATABASE_URL, echo=False)
            Base.metadata.create_all(engine)
            DBConnection.ENGINE = engine

        if not self.SESSION:
            self.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        DBConnection.SESSION = None

    @staticmethod
    def connect() -> None:
        """Creates a :class:`~.sqlalchemy.orm.scoping.scoped_session` and assigns it to :attr:`DBConnection.SESSION`"""
        DBConnection.SESSION = scoped_session(sessionmaker(bind=DBConnection.ENGINE))

    def query_profile(self, name: str) -> Query:
        """Queries the database for a :class:`~.Profile` by its name

        :param name: the profile name (ie. the :attr:`.Profile.name`)
        :returns: the :class:`~sqlalchemy.orm.Query` NOT the :class:`~.Profile`
        """
        return self.SESSION.query(Profiles).filter_by(name=name)

    def load_profile(self, name: str) -> InstaTweet.Profile:
        """Loads a profile from the database by name

        :param name: the profile name (ie. the :attr:`.Profile.name`)
        :raises LookupError: if the database has no profile saved with the specified name
        """
        if profile := self.query_profile(name).first():
            return pickle.loads(profile.config)
        else:
            raise LookupError(f"No database profile found with the name {name}")

    def save_profile(self, profile: InstaTweet.Profile, alert: bool = True) -> bool:
        """Saves a :class:`~.Profile` to the database by either updating an existing row or inserting a new one

        :param profile: the :class:`~.Profile` to save
        :param alert: if ``True``, will print a message upon successfully saving
        """
        if (db_profile := self.query_profile(profile.name)).first():
            db_profile.update({'config': profile.to_pickle()})
        else:
            new_profile = Profiles(name=profile.name, config=profile.to_pickle())
            self.SESSION.add(new_profile)

        self.SESSION.commit()

        if alert:
            print(f"Saved Database Profile: {profile.name}")
        return True

    def delete_profile(self, name: str, alert: bool = True) -> bool:
        """Deletes a :class:`~.Profile` from the database by name

        :param name: the profile name (ie. the :attr:`.Profile.name`)
        :param alert: if ``True``, will print a message upon successfully deleting
        """
        if not (profile := self.query_profile(name).first()):
            raise LookupError(f"No database profile found with the name {name}")

        profile.delete()
        self.SESSION.commit()

        if alert:
            print(f'Deleted Database Profile: {name}')
        return True
