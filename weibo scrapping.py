import time
from bs4 import BeautifulSoup #4.10.0
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from xlrd import open_workbook
from xlutils.copy import copy
import eventlet#导入eventlet这个模块


options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

# Set up the path to the ChromeDriver executable
service = Service(executable_path=r("/Users/huanglp/anaconda3/bin/chromedriver")

# Initialize the ChromeDriver with the Service object and options
driver = webdriver.Chrome(service=service, options=options)

 
base_url = "https://s.weibo.com/weibo?q=%23%E5%96%9C%E8%8C%B6%E5%81%A5%E5%BA%B7%E5%A4%BA%E5%86%A0%E7%BA%A4%E4%BD%93%E7%93%B6%23&page="

driver.get("https://weibo.com/p/100808ccb61d96c8f867d4f6c412e95c4f173a/super_index?current_page=3&since_id=4878245637659820&page=2#1678548112338")
driver.delete_all_cookies()
time.sleep(60)

driver.get(url)
time.sleep(5)
eventlet.monkey_patch()  # 必须加这条代码
with eventlet.Timeout(10, False):  # 设置超时时间为20秒
        while True:
            # 循环将滚动条下拉
            driver.execute_script("window.scrollBy(0,1000)")
            # sleep一下让滚动条反应一下
            time.sleep(0.05)
            # 获取当前滚动条距离顶部的距离
            check_height = driver.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            # 如果两者相等说明到底了
            if check_height >9000:
                break

elements = driver.find_elements_by_css_selector(
    "div.content p.txt a")
for i in elements:
    if "展开" in i.text:
        driver.execute_script("arguments[0].click()",i)

r_xls = open_workbook(r"/Users/huanglp/Desktop/weibo scrap.xlsx")  # 读取excel文件
row = r_xls.sheets()[0].nrows  # 获取已有的行数
excel = copy(r_xls)  # 将xlrd的对象转化为xlwt的对象
worksheet = excel.get_sheet(0)  # 获取要操作的sheet
    # 对excel表追加一行内容
for i in range(len(chuantong)):
    worksheet.write(row, 0, chuantong[i])  # 括号内分别为行数、列数、内容
 
    row += 1
excel.save(r"/Users/huanglp/Desktop/weibo scrap.xlsx")  # 保存并覆盖文件
