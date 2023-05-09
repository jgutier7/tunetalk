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
    image_url = Column(String) 
    prompt_option = Column(Integer)  
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, title, artist, user_id, prompt_option, genre=None, image_url=None):  # Update the constructor
        self.title = title
        self.artist = artist
        self.user_id = user_id
        self.prompt_option = prompt_option  
        self.genre = genre
        self.image_url = image_url 

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'genre': self.genre,
            'image_url': self.image_url,
            'prompt_option': self.prompt_option 
        }

    def __repr__(self) -> str:
        return f"Song(title='{self.title}', artist='{self.artist}', genre='{self.genre}', image_url='{self.image_url}', prompt_option={self.prompt_option})"


# from datetime import datetime

# class AIResponse(Base):
#     __tablename__ = 'ai_responses'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     song_id = Column(Integer, ForeignKey('songs.id'))
#     prompt = Column(Text, nullable=False)
#     response = Column(Text, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     def __init__(self, user_id, song_id, prompt, response):
#         self.user_id = user_id
#         self.song_id = song_id
#         self.prompt = prompt
#         self.response = response