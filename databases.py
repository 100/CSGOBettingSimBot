from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import mySettings

def createEngine():
	return create_engine(URL(**mySettings.DATABASE))

Base = declarative_base()

def createTables(engine):
	Base.metadata.create_all(engine)

class User(Base):
	__tablename__ = "users"

	username = Column(String, primary_key=True)
	currentMoney = Column(Float)
	wins = Column(Int)
	losses = Column(Int)
	netProfit = Column(Float)

class Match(Base):
	__tablename__ = "matches"
	
	id = Column(Int, primary_key=True)
	adjusted = Column(Boolean)

class Bet(Base):
	__tablename__ = "bets"

	commentID = Column(String, primary_key=True)
	matchId = Column(Int)
	team = Column(String)
	amount = Column(Float)
	

 
