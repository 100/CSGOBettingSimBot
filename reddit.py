import praw
import requests, requests.auth
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError
from mySettings import REDDIT as config
from databases import *

SCOPES = set(['edit','identity','privatemessages','read','submit'])
BOT_COMMANDS = ['bet','check']

def getToken():
	client_auth = requests.auth.HTTPBasicAuth(config['clientID'], config['secret'])
	post_data = {"grant_type": "password", "username": config['username'], "password": config['password']}
	headers = {"User-Agent": "CSGOBettingSimBot by /u/lavabender"}
	response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
	return dict(response.json())['access_token']

def createPRAW():
	r = praw.Reddit(user_agent="CSGOBettingSimBot by /u/lavabender")
	r.set_oauth_app_info(client_id=config['clientID'], client_secret=config['secret'],
		redirect_uri='http://127.0.0.1:65010/authorize_callback')
	r.set_access_credentials(SCOPES, getToken(), refresh_token=None, update_user=True)
	return r


def crawlSubmissions():
	r = createPRAW()
	matches = r.search('flair:"match"', subreddit = 'csgobetting')
	
	commentCommands = {}

	for match in matches:
		match.replace_more_comments(limit=None)
		flatComments = praw.helpers.flatten_tree(match.comments)
		botNamed = [comment for comment in flatComments if ("!"+config['username']).lower() in comment.body.lower()]
		for named in botNamed:
			if any("!"+config['username']+" "+command in named.body.lower() for command in BOT_COMMANDS):
				botNameIndex = named.body.lower().split().index("!"+config['username'])
				command = splitComment[botNameIndex + 1]
				commentCommands[named]=command

	return commentCommands

def bet(comment, session):
	submissionText = comment.submission.selftext

	try:	
		csglIndex = submissionText.index("[CSGL]")
	except ValueError:
		print "Submission does not contain any CSGL reference"
		return 
	
	csgoloungeLinkGeneric = "(http://csgolounge.com/match?m="
	
	if csgoloungeLinkGeneric in submissionText and (submissionText.indexcsgoloungeLinkGeneric) == csglIndex+1:
		matchID = int(submissionText[submissionText.index(csgoloungelinkGeneric)+1:submissionText.index(csgoloungelinkGeneric)+5])
		newMatch = Match(id = matchId, adjusted = False)
		
		try:
			session.add(newMatch)
			session.commit()
		except IntegrityError:
			pass
		except:
			session.rollback()

	try:
		author = comment.author.name
	except:
		pass
		return
	newUser = User(username = author, currentMoney = 0, wins = 0, losses = 0, netProfit = 0)
	try:
		session.add(newUser)
		session.commit()
	except IntegrityError:
		pass
	except:
		session.rollback()


	splitComment = comment.body.lower().split()
	
	botNameIndex = splitComment.index("!"+config['username'])
	betString = splitComment.index(botNameIndex + 2)
	teamString = splitComment.index(botNameIndex + 3).lower()
	
	try:	
		betAmount = float(betString)
	except ValueError:
		print "User did not provide a float as a bet"
		return 

	newBet = Bet(commentId = comment.id, user = author, matchId = matchID, team = teamString, amount = betAmount)
	try:
		session.add(newBet)
		session.commit()
	except IntegrityError:
		pass
	except:
		session.rollback()
	

def check(comment, session):
	try:
		userName = comment.author.name
	except:
		pass
		return

	try:
		user = session.query(User).filter(User.username == userName).one()
		subject = "Your Simulated Betting Status"
		message = "%s, you currently have %i wins and %i losses. The amount of money that you currently have is %f, and your net" 				"profit as of now is %f." % (user.username, user.wins, user.losses, user.currentMoney, user.netProfit)
	except (MultipleResultsFound, NoResultFound):
		subject = "There was a problem fetching your status..."
		message = "The bot was unable to fetch your information. Please make sure that you have made at least one bet, and that the" 				"match for that bet has already been completed."	

	r.send_message(userName, subject, message)
	
def processCommands(commands, session):
	for comment,command in commands.iteritems():
		if command == 'bet':
			bet(comment, session)
		if command == 'check':
			check(comment, session)







