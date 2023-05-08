from db_manager import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    songs = relationship('Song', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f"User(username='{self.username}')"


class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    genre = Column(String)
    image_url = Column(String)  # Add this line
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, title, artist, user_id, genre=None, image_url=None):  # Update the constructor
        self.title = title
        self.artist = artist
        self.user_id = user_id
        self.genre = genre
        self.image_url = image_url  # Add this line

    def __repr__(self) -> str:
        return f"Song(title='{self.title}', artist='{self.artist}', genre='{self.genre}', image_url='{self.image_url}')"

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String(80), unique=True, nullable=False)
#     password_hash = Column(String(120), nullable=False)
#     active = Column(Boolean, default=True)
#     def __init__(self, id, username, password, active=True):
#         self.id = id
#         self.username = username
#         self.password_hash = generate_password_hash(password)
#         self.active = active

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def is_active(self):
#         return self.active

#     def get_id(self):
#         return self.id

# class Song:
#     __tablename__ = 'songs'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=False)
#     artist = Column(String(255), nullable=False)
#     user_id = Column(Integer, ForeignKey(User.id))
#     def __init__(self, id, name, artist):
#         self.id = id
#         self.name = name
#         self.artist = artist
