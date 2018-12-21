from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

url = "https://www.coindesk.com/category/markets-news/markets-markets-news"
url = "https://www.ccn.com/"
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(5)
driver.get(url)

all_options = driver.find_elements_by_tag_name("button")
for i in range(len(all_options)):
    driver.get(url)
    options = driver.find_elements_by_tag_name("button")
    option = options[i]

    error_count = 0
    loop_count = 0
    last_lengths = [0]*20
    length = 1
    source = ""
    last_source = ""
    try:
        while driver.current_url == url  and error_count < 5 and len([i for i in last_lengths if i >= length]) < 20:
            print("starting while loop")
            try:
                print("Value is: %s" % option.get_attribute("value"))
                option.click()
                if driver.current_url != url:
                    logger.error("moved to new url" + str(driver.current_url) + " going back")
                    driver.back()
                err = False
            except:
                logger.exception("Tehere was an exception")
            time.sleep(0.5)

            last_source = source
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            last_lengths = last_lengths[1:]
            last_lengths.append(length)
            length = len(soup.find_all('a'))
    except:
        print("TIMEOUT EXCEPTION")

    if length > last_lengths[-1]:
        soup = BeautifulSoup(source, 'html.parser')
    else:
        soup = BeautifulSoup(last_source, 'html.parser')
    for link in soup.find_all('a'):
        print(link.get('href'))
    print("starting next iteration {}, errorcount = {} length = {},  last_length = {}".format(i, error_count, length,  last_lengths))



driver.close()
