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
    spotify_token = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    favorite_track = sqlalchemy.Column(sqlalchemy.String)
    favorite_artist = sqlalchemy.Column(sqlalchemy.String)

    top_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    top_tracks_short = sqlalchemy.Column(sqlalchemy.PickleType, nullable=True)
    top_tracks_medium = sqlalchemy.Column(sqlalchemy.PickleType, nullable=True)
    top_tracks_long = sqlalchemy.Column(sqlalchemy.PickleType, nullable=True)

    top_artists_short = sqlalchemy.Column(sqlalchemy.PickleType, nullable=True)
    top_artists_medium = sqlalchemy.Column(sqlalchemy.PickleType, nullable=True)
    top_artists_long = sqlalchemy.Column(sqlalchemy.PickleType, nullable=True)
