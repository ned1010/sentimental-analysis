from collections import defaultdict, Counter
import json
import string
from pathlib import Path
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import statistics
import csv


#Fetching the link to the json data
# Path(__file__).parent.absolute() 
current_path = str(Path().absolute())
link_to_data = current_path + "/lab3new/dataset/raw_singapore.json"


def analyse_sentiment(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    negative = score['neg']
    positive = score['pos']
    neutral = score['neu']
    compound = score['compound']
    return compound


new_hotel_details = list()

#Reading json/csv file with all the data 
with open(link_to_data) as f:
	data_content = json.loads(f.read())
for j in range(len(data_content)):
    total_polarity_score = 0
    temp_list = list()
    for k in data_content[j]['review']:
        print(k)
        current_review = k['comments']
        # Convert any uppercase letter to lowercase
        current_review = current_review.lower()
        # Remove any special character from the review comments 
        review_comments = current_review.translate(str.maketrans('', '', string.punctuation))
       
        #polarity score of the current review
        current_polarity_score = analyse_sentiment(review_comments)
        #accrue the total polarity score
        total_polarity_score += current_polarity_score
        #add the current polarity score to a temp list to calculate median later
        temp_list.append(abs(current_polarity_score))

    #after each hotel
    #time to add the relevant information about each hotel in new_hotel_details 
    #name, score, polarity_score_calculated, location
    new_hotel_details.append( [data_content[j]["name"], float(data_content[j]["overal_score"]), statistics.median(temp_list)*10, data_content[j]["location"],data_content[j]["latitude"],data_content[j]["longitude"], data_content[j]["imgSource"]] )

print("New hotel details are ")
print(new_hotel_details)
print(len(new_hotel_details))

to_dump_json_details = json.dumps(new_hotel_details, indent = 4)   
write_location = current_path + '/lab3new/dataset/sentiment/singapore_sentiment.json' 
with open(write_location, 'w') as file:
    file.write(to_dump_json_details) 
    file.close()

write_location = current_path + '/lab3new/dataset/sentiment/singapore_sentiment.csv'
with open(write_location, 'w', newline = '') as file:
    w = csv.writer(file)
    w.writerows(new_hotel_details)
    file.close()

#adding header names to the csv file just created. 
header_names = ["name", "score", "polarity score", "location", "latitude", "longitude","image_source"]
dw = csv.DictWriter(file, delimiter = ',', fieldnames=header_names)
file_address = current_path + '/lab3new/dataset/sentiment/singapore_sentiment.csv'
file = pd.read_csv(file_address)
file.to_csv(file_address, header=header_names, index=False)

