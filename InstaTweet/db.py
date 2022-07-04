from __future__ import annotations
import os
import pickle

from . import models, profile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


DATABASE_URL = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://', 1)
engine = create_engine(DATABASE_URL, echo=False)
Session = scoped_session(sessionmaker(bind=engine))


def query_profile(name):
    return Session.query(models.Profiles).filter_by(name=name)


def load_profile(name) -> profile.Profile:
    if db_profile := query_profile(name).first():
        return pickle.loads(db_profile.config)
    else:
        raise LookupError(f"No database profile found with the name {name}")


def save_profile(profile: profile.Profile, alert: bool = True) -> bool:
    """Updates profile if it already is saved, or adds it if not"""
    db_profile = query_profile(profile.name)
    if db_profile.first():
        db_profile.update({'config': profile.to_pickle()})
    else:
        new_profile = models.Profiles(name=profile.name, config=profile.to_pickle())
        Session.add(new_profile)
    Session.commit()

    if alert:
        print(f"Saved Database Profile: {profile.name}")
    return True


def delete_profile(name, alert: bool = True) -> bool:
    db_profile = query_profile(name)
    if not db_profile.first():
        raise LookupError(f"No database profile found with the name {name}")

    db_profile.delete()
    Session.commit()

    if alert:
        print(f'Deleted Database Profile: {name}')
    return True
