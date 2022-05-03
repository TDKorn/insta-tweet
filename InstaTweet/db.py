import os
import pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from InstaTweet.models import Profiles

DATABASE_URL = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://', 1)
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)


def load_profile(name):
    s = Session()
    db_profile = s.query(Profiles).filter_by(name=name).first()
    s.close()

    if db_profile:
        return pickle.loads(db_profile.config)
    return None


def save_profile(it):
    s = Session()
    pickle_string = pickle.dumps(it)
    db_profile = s.query(Profiles).filter_by(name=it.profile_name)

    if db_profile.first():
        db_profile.update({'config': pickle_string})
    else:
        s.add(Profiles(name=it.profile_name, config=pickle_string))

    s.commit()
    s.close()


def profile_exists(name):
    s = Session()
    db_profile = s.query(Profiles).filter_by(name=name).first()
    s.close()
    return bool(db_profile)
