'''
Script to return the top 10 hotels of all cities in 1 json file
'''


import json

from pathlib import Path

# sorting based on polarity

def polaritySort(data_content):	
	temp = sorted(data_content, key=lambda x: x[2])
	temp.reverse()
	
	return temp

def scoreSort(data_content):	
	temp = sorted(data_content, key=lambda x: x[1])
	temp.reverse()

	return temp

#Fetching the link to the json data
# Path(__file__).parent.absolute() 
def main():
	dataset = ["bangkok_sentiment", "singapore_sentiment", "kuala_lumpur_sentiment"]
	current_path = str(Path().absolute())
	all_hotel_polarity = []
	all_hotel_score = []
	for data in dataset:	
		link_to_data = current_path + "/lab3new/dataset/sentiment/"+data+".json"

		#Reading json/csv file with all the data 
		with open(link_to_data) as f:
			temp_content = json.loads(f.read())
			polarity_data = polaritySort(temp_content)
			score_data = scoreSort(temp_content)

			
			for i in range(0,10):
				all_hotel_polarity.append(polarity_data[i])
				all_hotel_score.append(score_data[i])

	#export data to json
	json_polarity = json.dumps(all_hotel_polarity, indent=4)
	json_score 	  = json.dumps(all_hotel_score,indent=4)

	write_location1 = current_path +"/lab3new/mapbox/src/data/all_hotel_polarity.json"
	with open(write_location1, 'w') as file:
		file.write(json_polarity) 
		file.close()

	write_location2 = current_path +"/lab3new/mapbox/src/data/all_hotel_score.json"
	with open(write_location2, 'w') as file:
		file.write(json_score) 
		file.close()

main()