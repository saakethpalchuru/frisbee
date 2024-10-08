# models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Association tables for many-to-many relationships
team1_players = Table('team1_players', Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id'), primary_key=True),
    Column('player_id', Integer, ForeignKey('players.id'), primary_key=True)
)

team2_players = Table('team2_players', Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id'), primary_key=True),
    Column('player_id', Integer, ForeignKey('players.id'), primary_key=True)
)

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    rating = Column(Float, default=1000)

    def __repr__(self):
        return f"<Player(name='{self.name}', rating={self.rating})>"

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    team1_score = Column(Integer, nullable=False)
    team2_score = Column(Integer, nullable=False)

    # Relationships
    team1_players = relationship('Player', secondary=team1_players, backref='games_as_team1')
    team2_players = relationship('Player', secondary=team2_players, backref='games_as_team2')

    def __repr__(self):
        return f"<Game(date={self.date}, team1_score={self.team1_score}, team2_score={self.team2_score})>"
