#selenium documentation
#https://selenium-python.readthedocs.io/
#https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys #gives access to keys to type, such as enter
import time
import json
from datetime import date

PATH = "C:\Program Files (x86)\Chromedriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)
today = str(date.today())
SEARCH_QUERY = "Steveston, Richmond BC"

JsonString = {}
JsonString["listing"] = []

def sendKeysSlowly(destination, keys):
    for i in range(len(keys)):
        destination.send_keys(keys[i])
        time.sleep(0.3)
        
def getNewPage():
    next_page = driver.find_element_by_xpath('//*[@id="ListViewPagination_Bottom"]/div/a[3]/div')
    #//*[@id="ListViewPagination_Bottom"]/div/a[3]/div
   # //*[@id="ListViewPagination_Bottom"]/div/div/span
    next_page.click()
    
def getListingCards():
    listing_cards_parent = driver.find_element_by_xpath('//*[@id="listInnerCon"]')
    listing_cards = listing_cards_parent.find_elements_by_class_name('cardCon')
    return listing_cards

def getListingPrice(i):
    listing_price = driver.find_element_by_xpath('//*[@id="listInnerCon"]/div[' + str(i) + ']/div/a/div/div[2]/div[1]/div[2]').get_attribute("title")
    return listing_price

def getAddress(i):
    address = driver.find_element_by_xpath('//*[@id="listInnerCon"]/div[' + str(i) +']/div/a/div/div[2]/div[1]/div[3]').get_attribute("innerText")
    return address
    
def getBedrooms(i):
    number_of_bedrooms = driver.find_element_by_xpath('//*[@id="listInnerCon"]/div[' + str(i) +']/div/a/div/div[2]/div[2]/div[1]/div[1]/div[1]').get_attribute("innerText")
    return number_of_bedrooms
    
def getBathrooms(i):
    number_of_bathrooms = driver.find_element_by_xpath('//*[@id="listInnerCon"]/div[' + str(i) +']/div/a/div/div[2]/div[2]/div[2]/div[1]/div[1]').get_attribute("innerText")
    return number_of_bathrooms
    
def getHouseType(i):
    house_type = driver.find_element_by_xpath('//*[@id="listInnerCon"]/div[' + str(i) +']/div/a/div/div[2]/div[2]/div[3]/div[2]').get_attribute("innerText")
    return house_type

def addToJsonString(price, address, bedrooms, bathrooms, housetype):
    JsonString["listing"].append({
                "list price": price,
                "address": address,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "house type": housetype})

def writeToJson():  
    with open(SEARCH_QUERY + "_" + today + ".json", "w") as write_file:
        json.dump(JsonString, write_file, indent=4, sort_keys=True)


def convertListingCardsToJson(listing_cards):
    for i in range(1, len(listing_cards) + 1):
        try:
            price = getListingPrice(i)
            address = getAddress(i)
            bedrooms = getBedrooms(i)
            bathrooms = getBathrooms(i)
            housetype = getHouseType(i)
            addToJsonString(price, address, bedrooms, bathrooms, housetype)
        except WebDriverException:
            pass
        
        
def getTotalPageNumbers():
    total_number_of_pages = driver.find_element_by_xpath('//*[@id="ListViewPagination_Bottom"]/div/div/div/span[2]').get_attribute("innerText")
    print(total_number_of_pages)
    return int(total_number_of_pages)

def getListingData():
    total_number_of_pages = getTotalPageNumbers()
    for i in range(total_number_of_pages):
        convertListingCardsToJson(getListingCards())
        getNewPage()
        time.sleep(5)

def zoom():
    zoom_button = driver.find_element_by_xpath('//*[@id="mapBodyCon"]/div/div/div[11]/div/div[2]/div/button[1]')
    zoom_button.click()
    zoom_button.click()
    time.sleep(1)
    
def setup():
    driver.get("https://www.realtor.ca/")
    time.sleep(6)
    search = driver.find_element_by_id("homeSearchTxt")
    sendKeysSlowly(search, SEARCH_QUERY)
    #search.send_keys("Williams Rd, Richmond BC") #what to type in the search box
    search.send_keys(Keys.RETURN) #hit enter
    time.sleep(30) #waits for the page to load
    #zoom()
    toggle_list_view = driver.find_element_by_xpath('//*[@id="mapViewToggle"]/div/div/a[2]')
    toggle_list_view.click()
    time.sleep(3)

def main():
    setup()
    getListingData()
    writeToJson()
    
#run  
main()

