import settings
import requests
import tweepy
import time
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#-----------------------------------------------------------------------------
# keyの指定(情報漏えいを防ぐため伏せています)
consumer_key = settings.CK
consumer_secret = settings.CS
access_token = settings.AT
access_token_secret = settings.ATC

# tweepyの設定(認証情報を設定)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# tweepyの設定(APIインスタンスの作成)
api = tweepy.API(auth)
#-----------------------------------------------------------------------------
#Yahoo天気から取得(文字列)
url = 'https://weather.yahoo.co.jp/weather/jp/8/4010.html'
url_text = requests.get(url)
soup = BeautifulSoup(url_text.text, 'html.parser')
li = soup.find(class_='contents-wide-table-body')
li = [i.strip() for i in li.text.splitlines()]
li = [i for i in li if i != ""]


#Yahoo天気から取得(画像)
# Chromeヘッドレスモード起動
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=options)
driver.implicitly_wait(10)

# ファイル名接頭辞
fileNamePrefix = 'image'

# ウインドウ幅指定
windowSizeWidth = 800

# ウインドウ高さ指定
windowSizeHeight = 600

# パス指定
folderPath = fileNamePrefix

# サイトURL取得
driver.get(url)
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
  
# ウインドウ幅・高さ指定
windowWidth = windowSizeWidth if windowSizeWidth else driver.execute_script('return document.body.scrollWidth;')
windowHeight = windowSizeHeight if windowSizeHeight else driver.execute_script('return document.body.scrollHeight;')
driver.set_window_size(windowWidth, windowHeight)

# 処理後一時待機
time.sleep(2)

# スクリーンショット格納
driver.save_screenshot('image.png')

# サーバー負荷軽減処理
time.sleep(1)

# ブラウザ稼働終了
driver.quit()

# 画像トリミング
im = Image.open('image.png')
im.crop((0, 330, 640, 550)).save('weather.png', quality=95)
#-----------------------------------------------------------------------------
#画像付きツイート
#api.update_status_with_media(status = 'おはようございます。\n今日の水戸の天気は' + li[1] + '。\n最高気温は' + li[2] + '、最低気温は' + li[3] + 'です。\n\nFrom Yahoo天気', filename = 'weather.png')
