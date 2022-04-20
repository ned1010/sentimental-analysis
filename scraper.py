
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

max_comment = 100
max_hotel = 20
current_path = str(Path().absolute())



def main():
	current_path = str(Path().absolute())
	location = str(input("Enter Location: "))

	#your path to the webdriver
	path = 'C:/Users/Dell/Desktop/Ashoka/SEMESTER4/Data Mining and Warehousing/Assignment/lab3/lab3new/chromedriver.exe'
	driver = webdriver.Chrome(path)
	driver.get('http://booking.com')

	searchField = driver.find_element_by_id("ss")
	searchField.send_keys(location)  ## pass in location
	searchField.send_keys(Keys.RETURN)


	finalData = get_hotel_data(driver, max_comment)

	link_to_data = current_path+"/lab3new/dataset/"

	print(finalData)	
	jsonData = [data for data in finalData]  # making data json compatable
	Data = json.dumps(jsonData, indent=4)
	with open(link_to_data+'raw_'+location+'.json', 'w') as f:
		f.write(Data)



	time.sleep(10)
	driver.quit()


def get_hotel_url(driver, maxNumber):
	#functin to return the urls of all the hotels for a particular location
	hotelUrl = []
	# hotelList = driver.find_elements_by_class_name('sr-hotel__title')
	# for hotel in hotelList:
	# 	url = hotel.find_element_by_class_name("hotel_name_link").get_attribute("href")
	# 	hotelUrl.append(url)
	

	counter = -1
	count = maxNumber - len(hotelUrl)

	while len(hotelUrl) < maxNumber-1:
		secondHotelList = driver.find_elements_by_class_name('sr-hotel__title')
		
		for hotel in secondHotelList:
			url = hotel.find_element_by_class_name("hotel_name_link").get_attribute("href")
			counter += 1
			urlLeft = count - counter
			# print(urlLeft)
			if urlLeft>0:
				hotelUrl.append(url) 
			else: 
				break

		if len(hotelUrl) == 0:
			print("Error: Check Location")

		driver.find_element_by_class_name('paging-next').click()
		time.sleep(2)

	print("Url fetch sucessful!!")
		
	return hotelUrl

def get_hotel_data(driver, maxComment):
	urls = get_hotel_url(driver, max_hotel)  #enter maximum hotel you want to search
	hotelData = []
	url_count = 0
	for url in urls:
		
		hotelDetails = {}

		driver.get(url)

		#scrape hotel name
		hotelDetails['name'] = driver.find_element_by_class_name('hp__hotel-name').text

		#scrape location data
		try:
			hotelDetails['location'] = driver.find_element_by_class_name('hp_address_subtitle').text
		except:
			hotelDetails['location'] = ''

		#scrape latitude and longtitude for mapbox
		latlong = driver.find_element_by_id('hotel_header').get_attribute("data-atlas-latlng")
		hotelDetails['latitude'], hotelDetails['longitude'] = latlong.split(",")

		#scrape hotel image
		hotelDetails['imgSource'] =driver.find_element_by_class_name('bh-photo-grid-item').get_attribute("href")
		
		#scrape score
		hotelDetails['overal_score'] = driver.find_element_by_class_name('bui-review-score__badge').text

		#scrape review breakdown
		hotelDetails['review_breakdown'] = {}
		for rating in  driver.find_elements_by_class_name('c-score-bar'):
			hotelDetails['review_breakdown'][rating.find_element_by_class_name('c-score-bar__title').text] = rating.find_element_by_class_name('c-score-bar__score').text

		

		#scrape reviews
		driver.find_element_by_class_name('hp_nav_reviews_link').click()
		reviews = [] # for indivdual hotel
		counter = -1
		count = maxComment - len(reviews)

		while len(reviews) < maxComment-1:

			wait = WebDriverWait(driver, 30)
			element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pagenext')))
			driver.find_element_by_class_name('pagenext').click()
			
			wait2 = WebDriverWait(driver, 30)
			element2 = wait2.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pagenext')))

			reviewList = driver.find_elements_by_class_name('review_list_new_item_block')
			
			for review in reviewList:
				reviewsDict = dict() # for each comment 
				try:
					reviewsDict['name'] = review.find_element_by_class_name('bui-avatar-block__title').text
				except:
					reviewsDict['name'] = ""

				# Fetch reviewer's date of posting review
				try:
					temp_date = review.find_element_by_class_name('c-review-block__date').text
					reviewsDict['date'] = temp_date
				except:
					reviewsDict['date'] = ""

				# Fetch reviewer's score given
				try:
					reviewsDict['score'] = review.find_element_by_class_name('bui-review-score__badge').text
				except:
					reviewsDict['score'] = ""

				# Fetch reviewers comment
				try:
					for rev in review.find_elements_by_xpath('.//span[@class = "c-review__body"]'):
						
						reviewsDict['comments'] = rev.text
				except:
					reviewsDict['comments'] = ''
				
				counter += 1
				reviewsLeft = count - counter
				if reviewsLeft>0:
					reviews.append(reviewsDict)
				else: 
					break	

			






		hotelDetails['review']	= reviews
		
		hotelData.append(hotelDetails)
		url_count += 1
		print("{}. Hotel Data Extraction Sucessful!".format(url_count))
	print("Data Extraction Completed!!")
	return(hotelData)

main()