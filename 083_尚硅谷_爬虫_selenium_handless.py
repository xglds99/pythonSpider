# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
#
# # path是你自己的chrome浏览器的文件路径
# path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# chrome_options.binary_location = path
#
# browser = webdriver.Chrome(chrome_options=chrome_options)
#
#
# url = 'https://www.baidu.com'
#
# browser.get(url)
#
# browser.save_screenshot('baidu.png')

# 封装的handless


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def share_browser():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # path是你自己的chrome浏览器的文件路径
    path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    chrome_options.binary_location = path

    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser

browser = share_browser()

url = 'https://www.baidu.com'

browser.get(url)
# 获取文本框的对象
input = browser.find_element("id",'kw')

# 在文本框中输入周杰伦
input.send_keys('周杰伦')

button = browser.find_element("id","su")
button.click()


