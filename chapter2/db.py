import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# declarative base class
# common to all tables in the application
# all models in the app derive from this base class
# Convention is to call this class 'Model'


class Model(DeclarativeBase):
    # Naming convention for constraints (instead of something random)
    # Helps better structure for the application
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })


load_dotenv()

# engine instance for managing DB connections and sessions
engine = create_engine(os.environ['DATABASE_URL'],
                       echo=True,
                       pool_size=10,  # default is 5
                       max_overflow=5,  # allow extra during spikes
                       future=True)  # Allow 2.0 APIs

# TODO: create_engine() docs

# This is different from sqlalchemy.orm.Session
# Instead of passing engine, pass the Session (maker) instance
# so that the functions can instantiate a Session in a context manager
SessionMaker = sessionmaker(engine, future=True)
