import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)

    link = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True, unique=True)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    spotify_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    spotify_auth_manager = sqlalchemy.Column(sqlalchemy.PickleType)

    favorite_track = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    favorite_artist = sqlalchemy.Column(sqlalchemy.String, nullable=True)
