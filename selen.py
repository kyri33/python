from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome()
driver.get('https://www.donna.co.za/browse/storeLocator.jsp')

element = driver.find_element_by_id('store-locator__search')
element.send_keys('gauteng')
element.send_keys(Keys.ENTER)

time.sleep(5)

titles = driver.find_elements_by_class_name('store-locator__store-title')
for title in titles:
    print(title.text)