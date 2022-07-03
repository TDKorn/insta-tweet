from __future__ import annotations
import os
import pickle
from .core.profile import Profile

from . import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


DATABASE_URL = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://', 1)
engine = create_engine(DATABASE_URL, echo=False)
Session = scoped_session(sessionmaker(bind=engine))


def query_profile(name):
    return Session.query(models.Profiles).filter_by(name=name)


def load_profile(name) -> "Profile":
    if db_profile := query_profile(name).first():
        return pickle.loads(db_profile.config)
    else:
        raise LookupError("No profile found with that name")


def save_profile(profile: Profile, alert: bool = True) -> bool:
    """Updates profile if it already is saved, or adds it if not"""
    db_profile = query_profile(profile.name)
    if db_profile.first():
        db_profile.update({'config': profile.to_pickle()})
    else:
        new_profile = models.Profiles(name=profile.name, config=profile.to_pickle())
        Session.add(new_profile)
    Session.commit()  # Unnecessary?
    if alert:
        print("Saved Profile " + profile.name)
    return True


def delete_profile(name):
    db_profile = query_profile(name)
    if not db_profile.first():
        raise LookupError("No profile found with that name")

    db_profile.delete()
    Session.commit()
    print('Deleted Profile' + name)

