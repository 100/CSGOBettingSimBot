import praw
import requests, requests.auth
from mySettings import REDDIT as config

SCOPES = set(['edit','identity','privatemessages','read','submit'])

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

