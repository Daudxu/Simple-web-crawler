import time
import re
from selenium import webdriver
from taskModel import taskJobModel
from time import sleep
from lxml import etree
from apscheduler.schedulers.blocking import BlockingScheduler
def task01():
    taskwebdriver()
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('自动确认发货定时任务-时间:', ts)
    time.sleep(2)

def taskwebdriver():
    driver = webdriver.Chrome(r"D:\\Program Files\chromedriver_win32\chromedriver.exe")
    print('打开网页')
    # 用get打开百度页面
    driver.get("https://www.huzhan.com")

    time.sleep(3)
    print('当前页面title', driver.title)
    print('当前页面url', driver.current_url)

    ul = driver.find_element_by_xpath('//*[@id="scrollDiv"]/ul')
    lis1 = ul.find_elements_by_xpath('li/*[@href]')
    lis2 = ul.find_elements_by_xpath('li/a/strong')
    lis3 = ul.find_elements_by_xpath('li/a/em')
    lis4 = ul.find_elements_by_xpath('li/a/span')

    # print(lis1)
    for link, name, money, goods in zip(lis1, lis2, lis3, lis4):
        s1 = link.get_attribute('href')
        s2 = name.get_attribute('innerHTML')
        s3 = money.get_attribute('innerHTML')
        s4 = goods.get_attribute('innerHTML')
        print(s1, 'is', s2, 'is', s3, "is", s4)

        taskObj = taskJobModel(s1,s2,s3,s4)
        taskObj.savedate()

    # len(lis)
    # driver.refresh()  # 刷新打开的页面
    print('关闭浏览器')
    driver.quit()

def dojob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间隔2S
    scheduler.add_job(task01, 'interval', seconds=20, id='test_job1')
    scheduler.start()

dojob()