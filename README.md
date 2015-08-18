# /r/csgobetting Simulator Bot 

This bot runs on the /r/csgobetting subreddit (https://www.reddit.com/r/csgobetting) on the popular website https://www.reddit.com. It interacts with the portion of the Counter-Strike: Global Offensive that is involved in betting in-game items on the results of professional tournaments and games, and allows users to make 'simulated' bets and monitor their money through this bot based on these real match events.

In order to use the bot, users must include their command to the bot in a particular format, and in the reddit submission that correlates with the match on which they wish to place their bets on. The bot is not case-sensitive for the most part; however, the portion of the command that conveys the type of command must be in lowercase (e.g. "bet" or "check). In addition, the bot only recognizes team names in the form that CSGL (csgolounge.com) uses on its match page (but is still case-insensitive). 

##This application uses:
* Python
* SQLAlchemy ORM
* PRAW API (Reddit API)
* CSGOLounge API

##Current Commands:
####Commands may be in any portion of a reddit post to the submission, so please, feel free to add it to the end of analysis posts.

* To place a bet: "!CSGOBettingSimBot bet [amount] [team]"
* To check one's current status: "!CSGOBettingSimBot check"


