from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://nga.178.com/read.php?tid=34604766&page=10")


while driver.title=='访客不能直接访问':
    time.sleep(0.1)

# click all '+' button
show_content_buttons=driver.find_elements(by=By.NAME,value='collapseSwitchButton')
for button in show_content_buttons:
    button.click()

res = driver.execute_cdp_cmd('Page.captureSnapshot', {})

with open('1.mhtml', 'w', newline='') as f:
    f.write(res['data'])

driver.quit()