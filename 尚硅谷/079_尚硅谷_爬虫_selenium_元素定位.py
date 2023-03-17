

from selenium import webdriver
from selenium.webdriver.common.by import By

path = 'chromedriver.exe'
browser = webdriver.Chrome(path)

url = 'https://www.baidu.com'
browser.get(url)

# 元素定位

# 根据id来找到对象

# button = browser.find_element("id","su")
# print(button)

# 根据标签属性的属性值来获取对象的
button1 = browser.find_element("name","wd")
# print(button)
print(button1)

# 根据xpath语句来获取对象
# button = browser.find_elements_by_xpath('//input[@id="su"]')
# print(button)
button2 =  browser.find_element("xpath","//input[@id='su']")
print(button2)
# //*[@id="train_date"]
# 根据标签的名字来获取对象
# button = browser.find_elements_by_tag_name('input')
# print(button)
button3 = browser.find_element("tag name","input")
print(button3)
# 使用的bs4的语法来获取对象
# button = browser.find_elements_by_css_selector('#su')
# print(button)
button4 = browser.find_element("css selector","#su")
print(button4)

# button = browser.find_element_by_link_text('直播')
# print(button)
button5 = browser.find_element(By.LINK_TEXT,"视频")
button5.click()