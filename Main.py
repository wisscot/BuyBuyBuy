
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

LOGINURL = r"https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_AccountFlyout_signout%26signIn%3D1%26useRedirectOnSuccess%3D1"
PRODUCT_URL = r"https://www.amazon.com/Ring-Fit-Adventure-Nintendo-Switch/dp/B07XV4NHHN/ref=sr_1_1?dchild=1&keywords=ring+fit&qid=1593802327&sr=8-1"

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
        url = "https://sc.ftqq.com/SCU99587T0e9e928545d18717051d27030eb41c025ecef193d432e.send"
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

