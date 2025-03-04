#importing libraries
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
#import dask.dataframe as dd

#importing datasets
dataset_movies = pd.read_csv('movies.csv')
dataset_rating = pd.read_csv('ratings.csv')
x_movies = dataset_movies.iloc[:, :-1].values
y_movies = dataset_movies.iloc[:, 2].values
x_rating = dataset_rating.iloc[:, :-1].values
y_rating = dataset_rating.iloc[:, 3].values

#Converting genres into catagory
from sklearn.preprocessing import LabelEncoder
labelencoder_y_movies = LabelEncoder()
y_movies[:] = labelencoder_y_movies.fit_transform(y_movies[:])

#using regEx for extracting release date from title
temp_rd = dataset_movies['title'].str.extract('(\(\d.{3})',expand=False)
dataset_movies['releaseDate'] = temp_rd.str.extract('(\d+)',expand=False)

#timestamp to timestamp_hour, timestamp_day, timestamp_year
dataset_rating['timestamp_hour'] = np.ceil(y_rating/3600)
dataset_rating['timestamp_day'] = np.ceil(y_rating/86400)
dataset_rating['timestamp_year'] = np.ceil(y_rating/31536000)

#merge datasets
merged = pd.merge(dataset_movies, dataset_rating, on = 'movieId')

#save merged as csv
merged.to_csv('joined.csv')

#sort merged dataset in ascending order based on movieId and timestamp_day
merged = merged.sort_values(['movieId','timestamp_day'], ascending= True)
merged.to_csv('sorted.csv')
#reset the index
merged = merged.reset_index(drop='True')

#preprocessing
#create variable for movieId and timestamp_day
mov = merged['movieId'].astype(str)
td = merged['timestamp_day'].astype(str)

#creating merged string (separated by '-')
merged['a'] = mov+'-'+td

#Creating label based on count from movieId and timestamp_day
ta= merged['a']
label = []
def rec(i, c):
    if i+1 < len(ta):
        if ta[i] == ta[i+1]:
            return rec(i+1, c+1)
    return i,c
i=0
while(i < len(ta)):
    count = 1
    if(i < len(ta)-1):
        temp, count = rec(i, count)
    temp+=1
    for p in range(i, temp):
        label.append(count)
    i = temp
    print(len(ta)-i)
lbl= pd.DataFrame(label)

#dropping 'a' column
merged = merged.drop(columns = 'a')

#merging label with previous dataset and saving the dataset in csv format
merged['label'] = lbl
merged.to_csv('preprocessed.csv')

#Splitting the dataset into Train and Test sets
from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(merged, test_size = 0.4, random_state = 0)
train_set.to_csv('training.csv')
test_set.to_csv('testing.csv')
