"""
pubmedの本日および昨日投稿された論文のURLとタイトルをSlackに朝7時(UTC夜10時)に自動送信する。
"""

# スクレイピング用ライブラリのインポート
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

# slack用ライブラリ
import tweepy, os

# サーバー上に設定したパスワードを取得
CONSUMER_KEY = os.environ["EMAIL"]
CONSUMER_SECRET = os.environ["PASSWORD"]
ACCESS_TOKEN = os.environ["token"]
ACCESS_TOKEN_SECRET = os.environ["channel_id"]

# 今日の日付を取得
today = datetime.today()
# print(datetime.strftime(today, '%Y %b %d'))
today_time = datetime.strftime(today, '%Y %b %d')

# 昨日の日付を取得
yesterday = today - timedelta(days=1)
# print(datetime.strftime(yesterday, '%Y %b %d'))
yesterday_time = datetime.strftime(yesterday, '%Y %b %d')


# 50ページまでスクレイピング
for i in range(51):
  # pubmedのページに飛び、BeuautifulSoupでスクレイピング
  page_link = 'https://pubmed.ncbi.nlm.nih.gov/?term=kidney&filter=datesearch.y_1&sort=date&page=' + str(i)
  # page_link = 'https://pubmed.ncbi.nlm.nih.gov/?term=kidney&filter=datesearch.y_1&sort=date' 
  res = requests.get(page_link).text
  soup = BeautifulSoup(res, 'html.parser')
  # 記事1つずつのタグを取得
  category_li_path = "section.search-results-list article.full-docsum"
  link_paths = soup.select(category_li_path)

  # 記事１つ分でforループ
  for link_path in link_paths:
      # 論文の日付を取得
      days_span = link_path.select('span.full-journal-citation')[0].text
      # 論文のタイトルとURLが含まれるaタグを取得
      title_url = link_path.select('a.docsum-title')
      if today_time in days_span:
        today_text = '本日投稿された論文です。'
        url = title_url[0].get("href")
        url_link = 'https://pubmed.ncbi.nlm.nih.gov' + str(url)
        title = title_url[0].text
        text = today_text + '\n' + url_link + '\n' + title
        # slackのurl,上記の内容をdataに記述
        url = "https://slack.com/api/chat.postMessage"
        data = {
          "token": ACCESS_TOKEN,
          "channel": ACCESS_TOKEN_SECRET,
            "text": text,
        }
        requests.post(url, data=data)
      elif yesterday_time in days_span:
        yesterday_text = '昨日投稿された論文です。'
        url = title_url[0].get("href")
        url_link = 'https://pubmed.ncbi.nlm.nih.gov' + str(url)
        title = title_url[0].text
        text = yesterday_text + '\n' + url_link + '\n' + title
        # slackのurl,上記の内容をdataに記述
        url = "https://slack.com/api/chat.postMessage"
        data = {
          "token": ACCESS_TOKEN,
          "channel": ACCESS_TOKEN_SECRET,
            "text": text,
        }
        requests.post(url, data=data)
        