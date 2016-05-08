#!/usr/bin/env python
import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import os
import os.path
import sys
import csv
import glob
import time
import datetime
from collections import defaultdict
import operator
from collections import Counter


# PATH TO track_metadat.db
# CHANGE THIS TO YOUR LOCAL CONFIGURATION
# IT SHOULD BE IN THE ADDITIONAL FILES
# (you can use 'subset_track_metadata.db')
dbfile = 'data/subset_track_metadata.db'
triplets_file_path = 'data/train_triplets.txt'
combined_path = 'data/song_user_count_combined.csv'

already_path = "data/already2.csv"

# connect to the SQLite database
# from that connection, get a cursor to do queries

# so there is no confusion, the table name is 'songs'
TABLENAME = 'songs'


def main():

    #if os.path.isfile("data/alreadyB.csv"):
      #  print "ACTUALLY EXISTS"

    # with open("data/check.csv", 'wb') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["hello1"])

    # with open("data/check.csv", 'a') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["hello2"])
    #generateUsersFiles()
    #print findTopNUsers(20)
    findTopNUsers(20)

def findTopNUsers(n):
    users_count = defaultdict(int)

    with open(already_path, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(csvreader):
            #print "a row  is", row 
            userId = row[0]
            users_count[userId] += 1

    sorted_users = sorted(users_count.items(), key=operator.itemgetter(0))

    counted_users = Counter(users_count)
    for k, v in counted_users.most_common(n):
        fileName = "data/usersData2/userId"+ k +".csv"
        newFileName = "data/topUsers2/userId"+ k +".csv"
        os.rename(fileName, newFileName)
        print k, v
    

    #return sorted_users[-20:]

def encode_string(s):
    """
    Simple utility function to make sure a string is proper
    to be used in a SQLite query
    (different than posgtresql, no N to specify unicode)
    EXAMPLE:
      That's my boy! -> 'That''s my boy!'
    """
    return "'"+s.replace("'","''")+"'"

def generateUsersFiles():
    header = ["user_id", "song_id", "song_play_count", "track_id", "title", "song_id", "release", "artist_id", "artist_mbid", "artist_name", "duration", "artist_familiarity", "artist_hottness", "year"]

    with open(combined_path, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(csvreader):
            if i != 0:
                #print "a full row is: ", row
                userId = row[0]
                #print "userId is:", userId
                fileName = "data/usersData2/userId" + userId + ".csv"
                if os.path.isfile(fileName):
                    #print "file " + fileName + "exists"
                    with open(already_path, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow([userId])
                    with open(fileName, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(row)
                else: 
                    #print "file " + fileName + "DOES NOT exist"
                    with open(fileName, 'wb') as f:
                        writer = csv.writer(f)
                        writer.writerow(header)
                        writer.writerow(row) 
                     
    #os.path.isfile(fname) 



def getTrainTriplets():
    tuples = []

    header = ["user_id", "song_id", "song_play_count", "track_id", "title", "song_id", "release", "artist_id", "artist_mbid", "artist_name", "duration", "artist_familiarity", "artist_hottness", "year"]
    
    with open('song_user_count_combined.csv', 'wb') as f:
        writer = csv.writer(f)
        # Write CSV Header, If you dont need that, remove this line
        writer.writerow(header)
        # for label, cluster, input_d in allZip:
        #     writer.writerow([label.encode("utf-8"), cluster, input_d[0], input_d[1]])
        for line in open(triplets_file_path, 'r'):
            split = line.split()
            #print " the split is: ", split
            songId = split[1]
            tup = (split[0], split[1], split[2])
            query_params = (songId,)
            #print songId
            q = "SELECT * FROM songs WHERE song_id = ?" 
            result = c.execute(q, query_params)
            found = result.fetchall()
            if len(found) > 0:
             #   print "found one! ", toAdd
                toAdd = list(found[0])
                encodedToAdd = [toAdd[0].encode("utf-8"), toAdd[1].encode("utf-8"), toAdd[2].encode("utf-8"), toAdd[3].encode("utf-8"), toAdd[4].encode("utf-8"), toAdd[5].encode("utf-8"), toAdd[6].encode("utf-8"), toAdd[7], toAdd[8], toAdd[9], toAdd[10]]
                combined_info_arr = split + encodedToAdd
                writer.writerow(combined_info_arr)

        # split + tuple(toAdd)
        #songsInfo.append(toAdd)
        #tuples.append(tup)

    return tuples


def getUserSongListeningCounts(songTriplets):
    songsInfo = []
    for songTriplet in songTriplets:
        songId = songTriplet[1]
        q = 'SELECT * FROM songs WHERE song_id =' + songId
        result = c.execute(q)
        toAdd = result.fetchall()
        print "a queryy: ", toAdd
        songsInfo.append(toAdd)

    return songsInfo


def setup(arrTuples):
    labels = [] 
    inputs = []

    for  artist, hotness, familiarity in arrTuples:
        inputs.append((float(hotness),float(familiarity)))
        labels.append(artist)

    labels = np.array(labels) 
    inputs = np.array(inputs)
    return (inputs, labels)


if __name__ == '__main__':
    # if len(sys.argv) < 4:
    #     print 'Usage: python process.py pinterest furniture_names stopwords'
    # pinterest_path = sys.argv[1]
    # furniture_names_path = sys.argv[2]
    # stopwords_path = sys.argv[3]
    main()

