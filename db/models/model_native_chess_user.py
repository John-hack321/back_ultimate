from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column , Text , Integer , String , Boolean , Enum , ForeignKey , DateTime

from db.models.mixins import TimeStamp
from db.db_setup import Base
from pydantic_schemas.chess_player_schemas import country_code
from pydantic_schemas.native_chess_player_schemas import GameVerdict

class NativeChessProfile(Base , TimeStamp):
    __tablename__ = "native_chess_profile"

    id = Column(Integer , primary_key = True , index = True , nullable = False)
    user_id = Column(Integer , ForeignKey('users.id') ,nullable = False)
    foreign_chess_id = Column(Integer , ForeignKey('chess_profile_table.id') , nullable = True)
    rating = Column(Integer , default = 0 )
    wins = Column(Integer , default = 0)
    loses = Column(Integer , default = 0)
    country = Column(Enum(country_code) , nullable = False , default = country_code.KE)

    native_games = relationship('NativeGames' , back_populates = "native_chess_profile")
    user = relationship("User" , back_populates = "native_chess_profile")

class NativeGames(Base , TimeStamp):
    __tablename__ = "native_games"

    id = Column(Integer , index = True , primary_key=True , nullable = False)
    native_chess_profile_id = Column(Integer , ForeignKey('native_chess_profile.id') , nullable = False)
    user_id = Column(Integer , ForeignKey('users.id'), nullable = False )
    played_as = Column(nullable = False)
    opponent = Column(String , nullable = False)
    verdict = Column(Enum(GameVerdict) , nullable = False)
    date = Column(DateTime , nullable = False , default = datetime.utcnow)
    start_time = Column(DateTime , default = datetime.utcnow, nullable = False)
    end_time = Column(DateTime)

    user = relationship('User' , back_populates="native_games")
    native_chess_profile = relationship('NativeChessProfile' , back_populates = "native_games")