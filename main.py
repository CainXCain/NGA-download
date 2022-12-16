from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time

url='https://nga.178.com/read.php?tid=34009511&authorid=61358733&page=4'
url=url.split('&')
for i in url:
    if i.find('page')!=-1:
        url.remove(i)
        break
url='&'.join(url)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# driver.get(url)

page_l=1
page_r=2

def page_exist(page):
    driver.get(url+'&page='+(str)(page))
    print(driver.title)
    elements=driver.find_elements(By.CLASS_NAME,value='uitxt1')
    for e in elements:
        if e.text=='后页':
            return True
    return False

while page_exist(page_r):
    page_r*=2
while page_l<page_r:
    mid=(page_l+page_r)//2
    if(page_exist(mid)):
        page_l=mid
    else:
        page_r=mid-1
pages=page_l

while driver.title=='访客不能直接访问':
    time.sleep(0.1)

title=driver.title.strip(' 178')

# click all '+' button
show_content_buttons=driver.find_elements(by=By.NAME,value='collapseSwitchButton')
for button in show_content_buttons:
    button.click()

res = driver.execute_cdp_cmd('Page.captureSnapshot', {})

with open(title+'.mhtml', 'w', newline='') as f:
    f.write(res['data'])

driver.quit()