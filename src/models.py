from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genres = Column(String)
    
    ratings = relationship("Rating", back_populates="movie")
    tags = relationship("Tag", back_populates="movie")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    
    ratings = relationship("Rating", back_populates="user")
    tags = relationship("Tag", back_populates="user")

class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    rating = Column(Float)
    timestamp = Column(Integer)
    
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    tag = Column(String)
    timestamp = Column(Integer)
    
    user = relationship("User", back_populates="tags")
    movie = relationship("Movie", back_populates="tags")
