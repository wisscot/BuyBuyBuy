
# from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
# import bs4
import time
import os
import sys
import pprint
import datetime
import random

LOGINURL = r"https://www.amazon.com/"
PRODUCT_URL = r"https://www.amazon.com/Ring-Fit-Adventure-Nintendo-Switch/dp/B07XV4NHHN/ref=sr_1_1?dchild=1&keywords=ring+fit&qid=1593802327&sr=8-1"
NOTIFY_URL = os.environ.get('ftqqURL')

class ChromeBrowser:

    def __init__(self, headless=False):
        
        if headless:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome()
        
    def login(self):
        if self.driver.current_url != LOGINURL: 
            self.driver.get(LOGINURL)  
            time.sleep(5)        
        
    def goto_product_page(self):
        if self.driver.current_url != PRODUCT_URL: 
            self.driver.get(PRODUCT_URL)  
            time.sleep(5)        
        
    def refresh(self):
        self.driver.refresh()
    
    def monitor_price(self, price_target = 80.0, interval = 5):
        driver = self.driver
        while True:
            elements = driver.find_elements_by_id("priceblock_ourprice")
            if len(elements) == 0:
                self.refresh()
                time.sleep(interval)
                continue
            
            price = float(elements[0].text[1:])
            if price < price_target:
                self.notify(f"Price of Fit Ring Dropped below {price_target:.2f}")
                # todo: logging
                buyNowButtons = driver.find_elements_by_id("buy-now-button")
                if not buyNowButtons:
                    time.sleep(interval)
                    print(time.ctime(), "there's no buyNowButton")
                    continue
                buyNowButtons[0].click()
                time.sleep(10)
                iframe = driver.find_element_by_id("turbo-checkout-iframe")
                driver.switch_to.frame(iframe)
                r = driver.find_elements_by_id("turbo-checkout-pyo-button")[0].click()
                print("place order response: ", r)
                
                return
            
    def notify(self, text):
        url = NOTIFY_URL
        url = url + f"?text={text} seed{random.randint(1,100)}"
        r = requests.get(url)
        print(r)
    
def main():
    chrome = ChromeBrowser()
    chrome.login()
    input('login first')
    chrome.goto_product_page()
    chrome.monitor_price(interval=5)
    
if __name__ == "__main__":
    main()

