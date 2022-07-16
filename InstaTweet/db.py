from __future__ import annotations
import os
import pickle
import InstaTweet

from sqlalchemy import create_engine, Column, String, LargeBinary
from sqlalchemy.orm import sessionmaker, scoped_session, Query
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = os.getenv('DATABASE_URL', '').replace('postgres://', 'postgresql://', 1)
Base = declarative_base()


class Profiles(Base):
    """Database table for :class:`Profile:profiles
    Config is just a pickle bytestring for now
    """
    __tablename__ = 'profiles'
    name = Column(String, primary_key=True)
    config = Column(LargeBinary)

    def __repr__(self):
        return "<Profiles(name='{}')>".format(self.name)


class DBConnection(object):
    """Database Connection class with context management ooh wow

    Sample Usage:
    >>> def poop_check():
    >>>     with DBConnection() as db:
    >>>         if db.query_profile(name="POOP").first() is None:
    >>>             print("Congrats, you're normal")
    >>>         else:
    >>>              raise EnvironmentError("Hostile")
    EnvironmentError: "Hostile"
    """

    SESSION = None

    def __enter__(self):
        if not self.SESSION:
            if not DATABASE_URL:
                raise EnvironmentError('DATABASE_URL not set')
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.SESSION.close()

    @staticmethod
    def connect():
        engine = create_engine(DATABASE_URL, echo=False)
        DBConnection.SESSION = scoped_session(sessionmaker(bind=engine))
        Base.metadata.create_all(engine)
        print('Connected to database')

    def query_profile(self, name: str) -> Query:
        """Execute a query by profile name. Call :meth:`~.Query.first`

        :param name: the profile name
        :return: the :class:`~sqlalchemy.orm.Query` NOT the :class:`~.Profile`
        """
        return self.SESSION.query(Profiles).filter_by(name=name)

    def load_profile(self, name: str) -> InstaTweet.Profile:
        """

        :param name:
        :return:
        """
        if profile := self.query_profile(name).first():
            return pickle.loads(profile.config)
        else:
            raise LookupError(f"No database profile found with the name {name}")

    def save_profile(self, profile: InstaTweet.Profile, alert: bool = True) -> bool:
        """Saves a :class:`~.Profile` to the database by either inserting a new row or updating an existing one

        :param profile:
        :param alert:
        :return:
        """
        if (profile := self.query_profile(profile.name)).first():
            profile.update({'config': profile.to_pickle()})
        else:
            new_profile = Profiles(name=profile.name, config=profile.to_pickle())
            self.SESSION.add(new_profile)

        self.SESSION.commit()

        if alert:
            print(f"Saved Database Profile: {profile.name}")
        return True

    def delete_profile(self, name: str, alert: bool = True) -> bool:
        """

        :param name:
        :param alert:
        :return:
        """
        if not (profile := self.query_profile(name).first()):
            raise LookupError(f"No database profile found with the name {name}")

        profile.delete()
        self.SESSION.commit()

        if alert:
            print(f'Deleted Database Profile: {name}')
        return True
