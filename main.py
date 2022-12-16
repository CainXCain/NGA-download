from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time

url='https://nga.178.com/read.php?tid=34713949'
#remove 'page= ' in url
url=url.split('&')
for i in url:
    if i.find('page')!=-1:
        url.remove(i)
        break
url='&'.join(url)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def skip_ads():#should use when opening any url
    if driver.title=='欢迎访问NGA玩家社区':
        skip=driver.find_element(by=By.ID,value='jump2')
        skip=skip.find_element(by=By.TAG_NAME,value='a')
        while True:
            try:
                skip.click()
                break
            except:
                time.sleep(0.1)
def driver_get(url):
    driver.get(url)
    while driver.title=='访客不能直接访问':
        time.sleep(0.1)
    skip_ads()

driver_get(url)
title=driver.title.strip(' 178')

#find out how many pages in this post
elements=driver.find_elements(By.CLASS_NAME,value='uitxt1')
flag=0
for e in elements:
    if e.text=='末页':
        flag=1
        e.click()
        skip_ads()
        elements=driver.find_elements(By.CLASS_NAME,value='uitxt1')
        break
pages=1
for e in elements:
    text=e.text[:-2+flag].strip()#last page id has special characters
    if text.isdigit():
        pages=max(pages,(int)(text)+flag)
#download
for i in range(1,pages+1):
    driver_get(url+'&page='+(str)(i))

    # click all '+' button
    show_content_buttons=driver.find_elements(by=By.NAME,value='collapseSwitchButton')
    for button in show_content_buttons:
        button.click()

    res = driver.execute_cdp_cmd('Page.captureSnapshot', {})

    with open(title+(str)(i)+'.mhtml', 'w', newline='') as f:
        f.write(res['data'])

driver.quit()