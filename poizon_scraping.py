from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import re
import pandas as pd
import time

url = "https://www.poizon.com/product/nike-dunk-low-panda-black-white-52581981"

def close_popup():
    try:
        driver.find_element(By.XPATH, '//*/button[@class="ant-modal-close"]').click()
    except Exception as error:
        print(error)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('user-agent=fake-useragent')
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(3)
close_popup()

driver.find_element(By.XPATH, '//*/div[starts-with(@class, "SkuPanel_sizeGuide")]').click()
time.sleep(3)
size_guide_table = driver.find_element(By.XPATH, '//*/div[@class="ant-modal-body"]/div/div[starts-with(@class, "size-guide_tableContainer")]/div[starts-with(@class, "size-guide_table")]').text
driver.find_element(By.XPATH, '//*/div[@class="ant-modal-body"]//div[starts-with(@class, "size-guide_unitList")]/div[text()="cm"]').click()
time.sleep(1)
cm_size_guide = driver.find_element(By.XPATH, '//*/div[@class="ant-modal-body"]/div/div[starts-with(@class, "size-guide_tableContainer")]/div[starts-with(@class, "size-guide_table")]/div[last()]').text
close_popup()
driver.close()

size_guide = size_guide_table.split('\n')
cm = cm_size_guide.split('\n')[1:]
size_guide_dict = {}
for t in size_guide:
    temp_list = []
    if re.findall('[A-Z|a-z]\w+', t):
        temp_key = t
        size_guide_dict[temp_key] = []
    else:
        size_guide_dict[temp_key].append(float(t))
size_guide_dict['Foot Length Fit (inch)'] = size_guide_dict.pop('Foot Length Fit')
size_guide_dict['Foot Length Fit (cm)'] = cm

size_guide_df = pd.DataFrame(size_guide_dict)
size_guide_df.to_csv('./data/poizon_size-guide.csv', index=False)