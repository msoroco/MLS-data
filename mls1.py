#selenium documentation
#https://selenium-python.readthedocs.io/
#https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium import webdriver
from selenium.webdriver.common.keys import Keys #gives access to keys to type, such as enter
import time

PATH = "C:\Program Files (x86)\Chromedriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)
#driver.minimize_window()

driver.get("https://www.youtube.com/?gl=CA")

search = driver.find_element_by_name("search_query")
search.send_keys("spring waltz") #what to type in the search box
search.send_keys(Keys.RETURN) #hit enter
time.sleep(5) #waits for the page to load
first_result = driver.find_element_by_xpath('//*[@id="video-title"]/yt-formatted-string')
first_result.click()



time.sleep(120)



driver.close() #closes current tab
driver.quit() #closes browser