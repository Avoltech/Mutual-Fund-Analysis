from selenium import webdriver
import pandas as pd 
import time
from selenium.webdriver.common.keys import Keys

df = pd.DataFrame(columns=['Fund Name', 'Fund Size', 
							'Largecap Holding', 'Midcap Holding', 
							'Smallcap Holding', 'Tinycap Holding',
							'Stocks Held', 'Stocks Sector', 'Percent Held'])

url = "https://www.etmoney.com/mutual-funds/all-funds-listing"

driver = webdriver.Chrome(r'C:/chromedriver/chromedriver.exe') 
driver.get(url)
time.sleep(3)

driver.find_element_by_xpath('//*[@id="categories"]/div[1]/div[1]/div').click()
driver.find_element_by_xpath('//*[@id="categories"]/div[1]/div[1]/div/button[1]').click()

consistency_range_slider = driver.find_element_by_id('consistencyRange')
for i in range(5):
  consistency_range_slider.send_keys(Keys.RIGHT)
time.sleep(2)


load_more = driver.find_element_by_class_name('load-more-nav-row')
try:
	while load_more:
		load_more.click()
		time.sleep(2)
		load_more = driver.find_element_by_class_name('load-more-nav-row')
except:
	#All records loaded
	pass

funds_list = driver.find_element_by_id('mfExplore_ListsItem')
funds_list = [i.find_element_by_tag_name('a') for i in funds_list.find_elements_by_class_name('scheme-name')]
fund_names = [i.text for i in funds_list]
fund_urls = [i.get_attribute('href') for i in funds_list]

for f in range(len(fund_urls)):
	fund_name = fund_names[f]
	fund_url = fund_urls[f]
	driver.get(fund_url)
	fund_size = driver.find_element_by_xpath('//*[@id="mfScheme-key-sec"]/div/div/table/tbody/tr[5]/td[2]/span[2]').text

	_id = fund_url.split('/')[-1]
	fund_url = fund_url.replace(_id, "portfolio-details/"+_id)
	driver.get(fund_url)

	large_cap_holding = driver.find_element_by_xpath('//*[@id="explore-home"]/div[6]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/p[1]').text
	mid_cap_holding = driver.find_element_by_xpath('//*[@id="explore-home"]/div[6]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/p[1]').text
	small_cap_holding = driver.find_element_by_xpath('//*[@id="explore-home"]/div[6]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/p[1]').text
	tiny_cap_holding = driver.find_element_by_xpath('//*[@id="explore-home"]/div[6]/div/div[2]/div[2]/div/div[4]/div[2]/div[1]/p[1]').text

	table = driver.find_element_by_xpath('//*[@id="explore-home"]/div[6]/div/div[6]/div/div/div[2]/div/table/tbody')
	tr_list = table.find_elements_by_tag_name('tr')
	stock_holding = []
	stock_sector = []
	holding_percent = []
	
	for td in tr_list:
		td_list = td.find_elements_by_tag_name('td')
		stock_holding.append(td_list[0].text)
		stock_sector.append(td_list[1].text)
		holding_percent.append(td_list[2].text)

	_row = {
		'Fund Name': fund_name,
		'Fund Size': fund_size,
		'Largecap Holding': large_cap_holding,
		'Midcap Holding': mid_cap_holding,
		'Smallcap Holding': small_cap_holding,
		'Tinycap Holding': tiny_cap_holding,
		'Stocks Held': stock_holding,
		'Stocks Sector': stock_sector,
		'Percent Held': holding_percent
	}
	df = df.append(_row, ignore_index=True)
df.to_csv("data.csv")