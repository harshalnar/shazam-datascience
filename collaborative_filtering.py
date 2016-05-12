from __future__ import division
from sklearn.neighbors import NearestNeighbors
import numpy as np
from sets import Set
import os
import os.path
import sys
import argparse
import csv
import math
import json
import random
import operator
from collections import defaultdict
from scipy.sparse import csc_matrix

users_interests = []
users_songs = []
index_song_map = {}

user_index_map = {}
userid_index_map = {}
index_userid_map = {}

ommited_songs = {}

def parse_args():
    parser = argparse.ArgumentParser(description='Collaborative Filtering of users')
    parser.add_argument('-u', help='user trying to get predictions from')
    return parser.parse_args()

def getPredictions(full_matrix, trainingSet, testSet):
    predictions = []

    no_index_testSet = []

    for userTuple in testSet:
        no_index_testSet.append(userTuple[1])

    user_similarities = getUserSimilarities(full_matrix)

    #print userTuple
    for userTuple in testSet:
        #print "generating similarities"
        user_suggestions_songIds = user_based_suggestions_songIds(userTuple[0], user_similarities)
        #print "suggestions are: ", user_suggestions_songIds

        #print index_song_map
        #good_predictions = user_suggestions_songIds[i]#map(lambda x: x[1], index_song_map.items())
        #print good_predictions
        #print len(good_predictions)
        #print len(index_song_map)
        good_predictions = []
        for i in range(10):   #<------------------NOTE: By changing this value you can make a nice graph
            #print "index is: ", i
            good_predictions.append(user_suggestions_songIds[i][0])

        predictions.append(set(good_predictions))

    return predictions


def getAccuracy(testSet, predictions):
    correct = 0.0
    #print "test set is: ", testSet
    for i, elem in enumerate(testSet):
        index = elem[0]
        user_listens = elem[1]
        #max_index, max_listen = max(enumerate(user_listens), key=operator.itemgetter(1))
        #most_listened_songId = index_song_map[max_index]

        #print "user listens: ", user_listens
        #print "max listens: ", max_listen
        #print "most listened songId: ", most_listened_songId
        #print "prediction: ", predictions[index]
        predictedSongs = map(lambda x: x[0], predictions[i])

        ommited_song_id = index_song_map[ommited_songs[index]]

        # predictedSongs.append(most_listened_songId)
        # print most_listened_songId in predictedSongs

        # NOTE: Weigh the values depending on the standing on predictions **********************
        if ommited_song_id in predictions[i]:
            correct += 1
        # print correct
    return (correct/float(len(testSet))) # * 100.0

# def dot(v1, v2):
# 	return sum(v1_i * v2_i for v1_i, v2_i in zip(v1, v2))

def cosine_similarity(v, w):
    return np.dot(v, w) / math.sqrt(np.dot(v, v) * np.dot(w, w))
 

# unique_songs = sorted(list({ interest 
#                                  for user_songs in users_songs
#                                  for interest in user_songs }))

def make_user_interest_vector(user_songs):
    """given a list of interests, produce a vector whose i-th element is 1
    if unique_songs[i] is in the list, 0 otherwise"""
    return [1 if interest in user_songs else 0
            for interest in unique_songs]



def getUserSimilarities(user_interest_matrix):
    user_similarities = [[cosine_similarity(interest_vector_i, interest_vector_j)
                      for interest_vector_j in user_interest_matrix]
                     for interest_vector_i in user_interest_matrix]
    return user_similarities

# user_interest_matrix = map(make_user_interest_vector, users_songs)

def getUniqueSongs():
	pass
	#unique_songs = []

def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def most_similar_users_to(user_id, user_similarities):

    #print "USER SIMILARITIES" , user_similarities
    #print "userID INDEX: ", user_id
    pairs = [(other_user_id, similarity)                      # find other
             for other_user_id, similarity in                 # users with
                enumerate(user_similarities[user_id])         # nonzero 
             if similarity > 0]                               # similarity

    return sorted(pairs,                                      # sort them
                  key=lambda (_, similarity): similarity,     # most similar
                  reverse=True)                               # first


def minMaxNormalize(minVal, maxVal, val):
    return float((float(val) - minVal)/(maxVal - minVal))



def getUserInterestMatrix(split, trainingSet=[], testSet=[]):
#XminmaxNorm = (X - min(X))/(max(X)-min(X))
    songIds = []
    userId = ""
    newSongs = []
    topUsers2_path = 'data/topUsers100/'
    song_set = Set([])
    users_info = []

    #users_interests = [Set([])]

    song_index_map = {}

    song_index = 0
    user_index = 0

    users_count = 0 
    songs_count = 0
    unique_songs = Set([])

    for filename in os.listdir(topUsers2_path):
        realPath = topUsers2_path + filename
        with open(realPath, 'rb') as csvfile:
            # each file is a user
            csvreader = csv.reader(csvfile, delimiter=',')
            users_count += 1
            for i, row in enumerate(csvreader):
                if i != 0:
                    songId = row[1] 
                    if songId not in unique_songs:
                        unique_songs.add(songId)
                        songs_count += 1




    user_interest_matrix = np.zeros((users_count, songs_count))

    for filename in os.listdir(topUsers2_path):
        realPath = topUsers2_path + filename
        user_interests = []
        user_songs = []
        with open(realPath, 'rb') as csvfile:
        	# each file is a user
            csvreader = csv.reader(csvfile, delimiter=',')
            user_info = {}
            user_heard = Set([])
            songPlayCounts = []
            user_index_map[filename] = user_index

            for i, row in enumerate(csvreader):
                if i != 0:

                    userId = row[0]
                    songId = row[1] 
                    songPlayCount = int(row[2])
                    songTitle = row[4]

                    userid_index_map[userId] = i
                    index_userid_map[i] = userId 
                    user_heard.add(songId)

                   # user_interest_matrix[user_index][song] = songPlayCount
                    user_interests.append(songId)
                    user_songs.append(songTitle)

                    if songId in song_index_map:
                        idx = song_index_map[songId]
                    	user_interest_matrix[user_index][idx] = songPlayCount

                    	
                    else: 
                        song_index_map[songId] = song_index 
                        index_song_map[song_index] = songId
                        user_interest_matrix[user_index][song_index] = songPlayCount
                        song_index += 1  

                      

    			#users_info.append({"user_heard": user_heard, "songPlayCounts": songPlayCounts})
            # split into training and test. 
            if random.random() < split:
                trainingSet.append(user_interest_matrix[user_index])
            else:
                max_index, max_listen = max(enumerate(user_interest_matrix[user_index]), key=operator.itemgetter(1))
                # most_listened_songId = index_song_map[max_index]
                #print user_interest_matrix[user_index]
                #print max_index
                #print max_listen
                #exit()
                # Set most listening song = 0, so we can test it later by finding it.
                user_interest_matrix[user_index][max_index] = 0;
                # Set each user in the testing list to the song taken out from it, so we can check later.
                ommited_songs[user_index] = max_index;

                testSet.append((user_index, user_interest_matrix[user_index]))      

    	    user_index += 1
            users_interests.append(user_interests)
            users_songs.append(user_songs)


    # print user_interest_matrix
    # sparse_R = csc_matrix(user_interest_matrix)

    # print sparse_R
    # print user_interest_matrix
    return user_interest_matrix

   	### FOR NORMALIZING LATER
  #  	for user in users_info:
  #  	   	user_interest_vector = [] 
  #  	   	songPlayCounts = user["songPlayCounts"]
  #  	   	userHeard = user["user_interests"]

  #  		for index, song in enumerate(unique_songs):
  #  			if song not in userHeard:
  #  				user_interest_vector[index] = 0
  #  			else: 
  #  				user_interest_vector[index] = songPlayCounts[]

  #  				## 0-1 Normalization.
  #  				#maxListenCount = max(songPlayCounts)
  #  				#minListenCount = min(songPlayCounts)
  #  				# value = minMaxNormalize(minListenCount, maxListenCount, row[2])
		#      #    if value >= 0.5:
		#      #        user_interest_vector[index] = 1 # give 1 if user likes song.
		#      #    else:
		#      #        user_interest_vector[index] = 0 # give 0 if user doesn't like song enough. 
		# user_interest_matrix.append(user_interest_vector)





    # for songInfo in unique_songs:
    #     row[2] = minMaxNormalize(minListenCount, maxListenCount, row[2])
    #     if row[2] >= 0.5:
    #         row[2] = 1 # give 1 if user likes song.
    #     else:
    #         row[2] = 0 # give 0 if user doesn't like song enough. 


    #print maxFamiliarity

#['user_id', 'song_id', 'song_play_count', 'track_id', 'title', 'song_id', 'release', 'artist_id', 'artist_mbid', 'artist_name', 'duration', 'artist_familiarity', 'artist_hottness', 'year']


def user_based_suggestions(user_id, user_similarities, include_current_interests=False):
    # sum up the similarities
    suggestions = defaultdict(float)
    most_similar_users = most_similar_users_to(user_id, user_similarities)

    for other_user_id, similarity in most_similar_users:
        for interest in users_songs[other_user_id]:
            suggestions[interest] += similarity

    # convert them to a sorted list
    suggestions = sorted(suggestions.items(),
                         key=lambda (_, weight): weight,
                         reverse=True)

    return suggestions
    # and (maybe) exclude already-interests
    # if include_current_interests:
    #     return suggestions
    # else:
    #     return [(suggestion, weight) 
    #             for suggestion, weight in suggestions
    #             if suggestion not in users_songs[user_id]]


def user_based_suggestions_songIds(user_id, user_similarities, include_current_interests=False):
    # sum up the similarities
    suggestions = defaultdict(float)
    most_similar_users = most_similar_users_to(user_id, user_similarities)

    #print "MOST SIMLAR USERS: ", most_similar_users
    for other_user_id, similarity in most_similar_users:
        # print other_user_id
        # print "**********"
        # print users_interests
        for interest in users_interests[other_user_id]:
            suggestions[interest] += similarity

    # convert them to a sorted list
    suggestions = sorted(suggestions.items(),
                         key=lambda (_, weight): weight,
                         reverse=True)

    return suggestions
    # and (maybe) exclude already-interests
    #if include_current_interests:
    #    return suggestions
    #else:
    #    return [(suggestion, weight) 
    #            for suggestion, weight in suggestions
    #            if suggestion not in users_interests[user_id]]


def main():
    args = parse_args()
    user = json.loads(args.u)[0]
    print user
    #plays = load_data("data/topUsers/userId13ce57b3a25ef63fa614335fd838e8024c42ec17.csv")
    #normalize("data/topUsers2/userId13ce57b3a25ef63fa614335fd838e8024c42ec17.csv")
    print "generating matrix"

    trainingSet = []
    testSet = []
    split = 2.0
    user_interest_matrix = getUserInterestMatrix(split, trainingSet, testSet)

    print "generating similarities"
    #user_similarities = getUserSimilarities(testSet)
    #print user_similarities

    # print "making suggestions"
    # #most_similar_users = most_similar_users_to(0, user_similarities)
    # user_suggestions = user_based_suggestions(0, user_similarities)
    # user_suggestions_songIds = user_based_suggestions_songIds(0, user_similarities)
    # print "SUGGESTIONS: "
    # print user_suggestions


    user_similarities = getUserSimilarities(user_interest_matrix)
    userid = user['idString']
    index = userid_index_map[userid]
    user_suggestions_songIds = user_based_suggestions_songIds(index, user_similarities)

    good_predictions = []
    for i in range(10):   #<------------------NOTE: By changing this value you can make a nice graph
        #print "index is: ", i
        good_predictions.append(user_suggestions_songIds[i][0])

    print good_predictions
    return good_predictions
    #predictions = getPredictions(user_interest_matrix, trainingSet, testSet)

    #no_index_testSet = []
    #for userTuple in testSet:
    #    no_index_testSet.append(userTuple[1])

    #accuracy = getAccuracy(testSet, predictions)

    #print "ACCURACY IS: ", accuracy

    #print user_suggestions_songIds
 #    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
	# nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
	# distances, indices = nbrs.kneighbors(X)


if __name__ == '__main__':
    main()




## USER-BASED COLLABORATIVE FILTERING: OUR APPROACH: 
# we have files for each user that: 
# multiple songs that each have: 
# userId and listening count. 

# our interest vector
