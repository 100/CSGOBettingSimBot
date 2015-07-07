from databases import *
import requests


def getToBeAdjusted(session):
	matchList = requests.get("http://csgolounge.com/api/matches")	

	unadjusted = session.query(User).filter(Match.adjusted == False).all()
	toBeAdjusted = {}		
	for unadjustedMatch in unadjusted:
		for match in matchList.json()[2500:]:
			if match['match'] == str(unadjustedMatch.id) and match['closed']=='1':
				toBeAdjusted[unadjustedMatch]=match
				break			
	return toBeAdjusted
		

def adjust(toBeAdjusted, session):
	for match,listElement in toBeAdjusted.iteritems():
		betsToAdjust = session.query(Bet).filter(Bet.matchId == match.id).all()
		if listElement['winner'] == 'c':
			for bet in betsToAdjust:
				user = session.query(User).filter(User.username == bet.user).one()
				user.currentMoney += bet.amount
				session.delete(bet)
				try:				
					session.commit()
				except:
					session.rollback()			
		else:
			wonBets = [bet for bet in betsToAdjust if bet.team.lower() == listElement[listElement['winner']].lower()]
			lostBets = [bet for bet in betsToAdjust if bet not in wonBets]
			for bet in betsToAdjust:
				user = session.query(User).filter(User.username == bet.user).one()
				if bet in wonBets:
					user.currentMoney += bet.amount + (bet.amount * getMultiplier(listElement, bet))
					user.wins += 1
					user.netProfit += bet.amount * getMultiplier(listElement, bet)
				else:
					user.currentMoney += -bet.amount
					user.losses += 1
					user.netProfit += -bet.amount
				session.delete(bet)
				try:				
					session.commit()
				except:
					session.rollback()					
				
		match.adjusted = True
		session.delete(match)
		try:				
			session.commit()
		except:
			session.rollback()

def getMultiplier(matchDict, bet):
	matchStats = requests.get("http://csgolounge.com/api/matches").json()[2500:]
	for stat in matchStats:
		if stat['match'] == matchDict['match']:
			if bet.team.lower() == matchDict['a'].lower():
				return 1 / (float(stat['a']) / float(stat['b']))
			else:
				return 1 / (float(stat['b']) / float(stat['a']))
			
				
			
		
		
	
