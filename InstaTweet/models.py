from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, LargeBinary

Base = declarative_base()


class Profiles(Base):
    __tablename__ = 'profiles'
    name = Column(String, primary_key=True)
    config = Column(LargeBinary)

    def __repr__(self):
        return "<Profiles(name='{}')>".format(self.name)

