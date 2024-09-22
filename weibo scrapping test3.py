import time
from bs4 import BeautifulSoup #4.10.0
from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from xlrd import open_workbook
from xlutils.copy import copy
from openpyxl import load_workbook
import eventlet#导入eventlet这个模块
import pandas as pd
import os

# Path to your ChromeDriver
chrome_driver_path = '/Users/huanglp/anaconda3/bin/chromedriver'

# Path to your Chrome binary
chrome_binary_path = '/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome'

chrome_options = Options()
chrome_options.binary_location = chrome_binary_path

# Initialize the ChromeDriver service
service = Service(chrome_driver_path)

# Initialize the WebDriver with options and service
web = webdriver.Chrome(service=service, options=chrome_options)

base_url = "https://s.weibo.com/weibo?q=%E5%96%9C%E8%8C%B6%E7%BA%A4%E4%BD%93%E7%93%B6&page="
# Your test code here
web.get("https://weibo.com/p/100808ccb61d96c8f867d4f6c412e95c4f173a/super_index?current_page=3&since_id=4878245637659820&page=2#1678548112338")
web.delete_all_cookies()
time.sleep(30)
# Refresh the page to apply the cookies
web.refresh()

def save_data(web_data, filename):
    # Define the column names
          fieldnames = ['text', 'date', 'user_name', 'gender', 'repost_num', 'comment_num', 'like_num']
          df = pd.DataFrame(web_data, columns=fieldnames)

          if os.path.exists(filename):
        # If the file exists, append data to it
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
               df.to_excel(writer, index=False, sheet_name='Sheet2')
          else:
        # If the file does not exist, create it and write data
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
               df.to_excel(writer, index=False, sheet_name='Sheet2')

data=[]
for i in range(20,50):
    web.get(base_url + str(i))
    WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    last_height = web.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down
        web.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new content to load
        time.sleep(10)  # Adjust sleep time as needed
        
        # Calculate new height and compare with the last height
        new_height = web.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    html = web.page_source
    soup = BeautifulSoup(html, 'html.parser')
    list = soup.findAll("div", {'action-type': "feed_list_item"})

    html = web.page_source
        # 获取这一网页的所有未展开的文章的展开按钮
    button_list = web.find_elements(By.CSS_SELECTOR, 'a[action-type="fl_unfold"]') #点击所有展开
        # 在for循环里面每个都点击展开
    for bt in button_list:
        try :
            bt.click()
        except Exception as e:
            print(e.args)
        # html转beautifulsoup格式
    soup = BeautifulSoup(html, 'html.parser')
        # 已经展开了，开始正常获取这一页的微博列表list
    list = soup.findAll("div", {'action-type': "feed_list_item"})
    for i in list:
        web_object = {}
        txt = i.findAll("p", {'class':"txt"})[-1].get_text().strip()
        web_object['text'] = txt
        user_name = i.find("a", {'class': "name"}).get_text()#名字放在class为name的a标签里面
        web_object['user_name'] = user_name
        i = i.find("div",{'class':"card"})
        itime = i.find("div", {'class': "from"})
        uptime = itime.find("a").get_text().strip()
        web_object['date'] = uptime
        cardact = i.find("div", {'class': "card-act"})
        repost_num = cardact.findAll("li")[0].get_text().strip()
        if repost_num =="转发":
            repost_num = 0
        web_object['repost_num'] = repost_num
        comment_num = cardact.findAll("li")[1].get_text().strip()
        if comment_num == "评论":
            comment_num = 0
        web_object['comment_num'] = comment_num
        like_num = cardact.findAll("li")[2].get_text().strip()
        if like_num == "赞":
            like_num =0
        web_object['like_num'] = like_num
            
    # 控制跳转
        user_link=i.find("a").get("href")
        print("用户主页：", user_link)
        web_object['user_link'] = user_link# 拼出用户的主页链接user_url
        user_url = "'" + "https:" + user_link+ "'"
        js = "window.open(" + user_url + ");"
        web.execute_script(js)
        time.sleep(2)
        window_1 = web.current_window_handle# 获得打开的所有的窗口句柄
        windows = web.window_handles# 切换到最新的窗口
        for current_window in windows:
            if current_window != window_1:
                    web.switch_to.window(current_window)
        html = web.page_source
        soup = BeautifulSoup(html, 'html.parser')
        print("切换到用户主页")
        genderhtml = soup.find("div",{'class': "woo-box-flex woo-box-alignCenter ProfileHeader_h3_2nhjc"})
        gender = genderhtml.find("span").get("title").strip()
        web_object['gender'] = gender
        web.close()
        web.switch_to.window(window_1)
        data.append(web_object)
        print(web_object)


filename ='/Users/huanglp/Desktop/weibo scrap.xlsx'
save_data(data,filename)
web.quit()










