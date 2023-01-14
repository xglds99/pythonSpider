

from selenium import webdriver
from selenium.webdriver.common.by import By

path = 'chromedriver.exe'
browser = webdriver.Chrome(path)


url = 'http://www.baidu.com'
browser.get(url)


input = browser.find_element("id","su")

# 获取标签的属性
print(input.get_attribute('class'))
# 获取标签的名字
print(input.tag_name)

# 获取元素文本
a = browser.find_element(By.LINK_TEXT,'新闻')
print(a.text)

