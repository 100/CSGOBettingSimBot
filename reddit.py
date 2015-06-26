import praw
import requests, requests.auth
from mySettings import REDDIT as config

SCOPES = set(['edit','identity','privatemessages','read','submit'])
BOT_COMMANDS = {'bet':bet, 'check':check}

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
		flat_comments = praw.helpers.flatten_tree(match.comments)
		botNamed = [comment for comment in flat_comments if ("!"+config['username']).lower() in comment.body.lower()]
		for named in botNamed:
			if any("!"+config['username']+" "+command in named.body.lower() for command in BOT_COMMANDS.values()):
				commentCommands[comment]=command

	return commentCommands

def bet(comment): ###Update database
#Takes in comment, needs to parse string for amount/team, look for CSGL link in original submission, update databases
#UPDATE THE BET TABLE AND MATCHES TABLE - will update the other table later on based on csgolounge api
#NEED TO IMPORT sessionmaker, etc FOR DATABASE COMMUNICATION


def check(comment): ###PM user with their info
#Checks database for that username, sends a PM with info formatted

		
def processCommands(commands):
	for comment,command in commands.iteritems()
		commands[comment](comment)







