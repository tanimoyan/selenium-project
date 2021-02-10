from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


# 列名が["title", "url"]である、データフレームを作成
columns = ["title", "url"]
df = pd.DataFrame(columns=columns)

# Seleniumのパスを通して、ログインページにアクセスする
options = Options()
options.add_argument('--headless') 
browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options) 
browser.get("https://crowdworks.jp/public/jobs/search?search%5Bkeywords%5D=python&keep_search_criteria=true&order=new&hide_expired=false")


# 全件取得
# 次へがなくなるまでforループ
while True:
    item_slctrs = browser.find_elements_by_css_selector("div.search_results > ul.jobs_lists > li")
    for item in item_slctrs:
        title = item.find_element_by_css_selector("h3.item_title").text
        url = item.find_element_by_css_selector("h3.item_title a").get_attribute("href")
        # DataFrameに、スクレイピングした結果を追加
        se = pd.Series([title, url], columns)
        df = df.append(se, ignore_index=True)
        print (df)
               
               
    try:
        next_slctr = browser.find_element_by_xpath("//a[@rel='next']")
        if next_slctr:
            next_url = next_slctr.get_attribute("href")
            print ("move to {}".format(next_url))
            browser.get(next_url)
            continue
    except:
        break

# csvファイルをエクスポート
df.to_csv("result.csv")