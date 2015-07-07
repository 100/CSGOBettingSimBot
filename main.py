from mySettings import *
from databases import *
from reddit import *
from checkResults import *
from sqlalchemy.orm import sessionmaker

def main():
	engine = createEngine()
	createTables(engine)
	sessionMaker = sessionmaker(bind=engine)
	session = sessionMaker()

	processCommands(crawlSubmissions(), session)
	adjust(getToBeAdjusted(session), session)

	print session.query(Bet).all()

main()
