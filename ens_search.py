from selenium_driverless.sync import webdriver
import time
import requests
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
url = "https://app.ens.domains/{}.eth"

# read names
f = open('names.txt', 'r', encoding='utf-8')
names = []
for line in f.readlines():
    real_name = line.replace('\n', '')
    names.append(real_name)
f.close()
names = list(set(names))

print(url.format(names[0]))
f = open('available_ens.txt', 'a', encoding='utf-8')
f.write('\n')
for name in names:
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.sleep(0.5)
        time.sleep(1)
        #driver.wait_for_cdp("Page.domContentEventFired", timeout=15)

        title = driver.title
        url = driver.current_url
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        expiry = soup.find('button', {'data-testid' : 'owner-profile-button-name.expiry'})
        if (not expiry): # register available
            f.write(name + '\n')

f.close()
    