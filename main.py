from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

import time
import os

path=os.path.dirname(os.path.abspath(__file__))

url='https://nga.178.com/read.php?tid=35309665&_ff=806&page=18'
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
path=os.path.join(path,title)
os.makedirs(path,exist_ok=True)

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

#edit here
start=1
end=pages

#download
for i in range(start,end+1):
    driver_get(url+'&page='+(str)(i))

    # close '界面设置'
    settings=driver.find_elements(by=By.CLASS_NAME,value='single_ttip2')
    if len(settings)!=0:
        clost_button=settings[0].find_element(by=By.CLASS_NAME,value='colored_text_btn')
        clost_button.click()

    # click all '+' button
    show_content_buttons=driver.find_elements(by=By.NAME,value='collapseSwitchButton')
    for button in show_content_buttons:
        button.click()
    
    # click '显示图片' in replies
    show_img_buttons=driver.find_elements(by=By.TAG_NAME,value='button')
    for button in show_img_buttons:
        if button.text=='显示图片':
            button.click()

    #srcoll to images not loaded and wait until the last one is loaded
    imgs=driver.find_elements(by=By.TAG_NAME,value='img')
    last_img=0
    for img in imgs:
        if img.get_attribute('src')=='about:blank' and img.get_attribute('style')!='display: none;':
            ActionChains(driver)\
                .scroll_to_element(img)\
                .perform()
            last_img=img
    if last_img!=0:
        try:
            WebDriverWait(driver,timeout=5).until(lambda d:last_img.get_attribute('src')!='about:blank')
        except:
            last_img=last_img

    res = driver.execute_cdp_cmd('Page.captureSnapshot', {})

    with open(os.path.join(path,(str)(i)+'.mhtml'), 'w', newline='') as f:
        f.write(res['data'])

driver.quit()