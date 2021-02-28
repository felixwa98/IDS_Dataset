from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configparser import SafeConfigParser
import platform
import sys
import time
import re
import os
import random
import linecache
import getpass
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)
import Packages.logging.log_file as log



def choose_random_url(urllist):
    lines = open(urllist).read().splitlines()
    url = random.choice(lines)
    return url

# Youtube (URL aufrufen und ein paar Min schauen ?

def watch_youtube(urllist):

    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 3)
    presence = EC.presence_of_element_located
    visible = EC.visibility_of_element_located

    url = choose_random_url(urllist)

    driver.get(url)

    log.log_event("HTTP; Start Video;"+str(url))

    # play the video
    wait.until(visible((By.ID, "video-title")))
    driver.find_element_by_id("video-title").click()

    time.sleep(random.randint(60,180))

    driver.quit()
    log.log_event("HTTP; Stop Video;"+str(url))






# Suchen von Begriffen (Google + 1 -3 Ergebnisse

def use_google(searchlist):
    driver = webdriver.Firefox()

    searchword = choose_random_url(searchlist)

    url = "https://www.google.com/search?q=" + searchword

    driver.get(url)

    log.log_event("HTTP; Google Search;"+str(searchword))

    links = driver.find_elements_by_class_name('g')

    counter = 0
    max_links =random.randint(1,3)

    time.sleep(random.randint(20,60))

    for link in links:
        counter += 1
        url = link.find_element_by_tag_name('a').get_attribute("href") 
        driver.execute_script('''window.open("{}","_blank");'''.format(url)) 
        log.log_event("HTTP; Google Search Result;"+str(url))

        if counter >= max_links:
            break
        else:
            time.sleep(random.randint(40,60*3))

    driver.quit()



# Newsseiten + 1-3 Artikel

def get_news(urllist):
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 3)

    url = choose_random_url(urllist)
    

    max_links =random.randint(1,3)


    for i in range(0,max_links):

        url = choose_random_url(urllist)
        driver.get(url)

        log.log_event("HTTP; News;" + str(url))
        time.sleep(random.randint(10,60*3))



    driver.quit()


def main(videolist, searchlist, newslist):

    make_choose = random.randint(1,3)

    if (make_choose == 1):
        try:
            watch_youtube(videolist)
        except:
            log.log_event("HTTP; fail to watch youtube")
    elif (make_choose == 2):
        try:
            use_google(searchlist)
        except:
            log.log_event("HTTP; fail to google")
    elif (make_choose == 3):
        try:
            get_news(newslist)
        except:
            log.log_event("HTTP; fail to get news")
    

