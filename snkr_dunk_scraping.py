from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

url = 'https://snkrdunk.com/en/sneakers/DD1391-100'

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


size_chart_men = driver.find_element(By.XPATH, '//*/div[@class="size-chart__table"]').text
driver.find_element(By.XPATH, '//*/div[@class="size-chart__wrapper"]//li[@class="size-chart__tab-item"]/a').click()
size_chart_women = driver.find_element(By.XPATH, '//*/div[@class="size-chart__table"]').text

men_dict = dict()
for s in size_chart_men.split('\n')[0].split():
    men_dict[s] = []
for s in size_chart_men.split('\n')[1:]:
    men_dict['US'].append(float(s.split(' ')[0]))
    men_dict['UK'].append(float(s.split(' ')[1]))
    men_dict['EU'].append(float(s.split(' ')[2]))
    men_dict['CM'].append(float(s.split(' ')[3]))

women_dict = dict()
for s in size_chart_women.split('\n')[0].split():
    women_dict[s] = []
for s in size_chart_women.split('\n')[1:]:
    women_dict['US'].append(float(s.split(' ')[0]))
    women_dict['UK'].append(float(s.split(' ')[1]))
    women_dict['EU'].append(float(s.split(' ')[2]))
    women_dict['CM'].append(float(s.split(' ')[3]))

men_df = pd.DataFrame(men_dict)
women_df = pd.DataFrame(women_dict)

driver.find_element(By.XPATH, '//*/div[@class="product-detail__select"]/a').click()
time.sleep(5)

size2price_list = driver.find_elements(By.XPATH, '//*/div[@class="choose-size"]/ul/li')
size2price_list = [s2p.text for s2p in size2price_list]

size2price_df = pd.DataFrame({"size":[s.split('\n')[0] for s in size2price_list], "price": [s.split('\n')[-1] for s in size2price_list]})
size2price_df['price'] = size2price_df['price'].replace('coming soon', '-')

men_df.to_csv('./data/snkr_dunk_men-size.csv', index=False)
women_df.to_csv('./data/snkr_dunk_women-size.csv', index=False)
size2price_df.to_csv('./data/snkr_dunk_price-by-size.csv', index=False)

driver.close()