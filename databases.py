from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import mySettings

def createEngine():
	return create_engine(URL(**mySettings.DATABASE))

Base = declarative_base()

def createTables(engine):
	Base.metadata.create_all(engine)

class User(Base):
	__tablename__ = "users"

	username = Column(String(50), primary_key=True)
	currentMoney = Column(Float)
	wins = Column(Integer)
	losses = Column(Integer)
	netProfit = Column(Float)

class Match(Base):
	__tablename__ = "matches"
	
	id = Column(Integer, primary_key=True)
	adjusted = Column(Boolean)

class Bet(Base):
	__tablename__ = "bets"

	commentId = Column(String(50), primary_key=True)
	user = Column(String(50))
	matchId = Column(Integer)
	team = Column(String(50))
	amount = Column(Float)
	

 
