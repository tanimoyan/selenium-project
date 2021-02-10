"""
Slackにファイルをアップするコード
"""


import requests
import tweepy, os

CONSUMER_KEY = os.environ["EMAIL"]
CONSUMER_SECRET = os.environ["PASSWORD"]
ACCESS_TOKEN = os.environ["token"]
ACCESS_TOKEN_SECRET = os.environ["channel_id"]

url = "https://slack.com/api/files.upload"
data = {
   "token": ACCESS_TOKEN,
   "channels": ACCESS_TOKEN_SECRET,
   "title": "my file",
   "initial_comment": "initial\ncomment"
}
filename = '/home/ec2-user/environment/selenium_project/result.csv'
files = {'file': open(filename, 'rb')}
requests.post(url, data=data, files=files)