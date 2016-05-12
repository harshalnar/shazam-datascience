from __future__ import division
from sklearn.neighbors import NearestNeighbors
import numpy as np
from sets import Set
import os
import os.path
import bson
import sys
import csv
import json 
import math
import string
import random
import names 
import operator
from collections import defaultdict
from scipy.sparse import csc_matrix

used_names = Set([])

users_interests = []
users_songs = []
index_song_map = {}

user_index_map = {}
userid_index_map = {}

ommited_songs = {}

def findTriple(userHex, songHex, triples):
    for i, triple in enumerate(triples):
        if triple['user'] == userHex and triple['song'] == songHex:
            return i 

toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])

def getUserInterestMatrix():
#XminmaxNorm = (X - min(X))/(max(X)-min(X))
    songIds = []
    userId = ""
    newSongs = []
    topUsers2_path = '../data/topUsers100/'
    song_set = Set([])
    users_info = []

    songs = []
    users = []
    triples = []

    #users_interests = [Set([])]

    song_index_map = {}

    # unique_songs = Set([])

    for filename in os.listdir(topUsers2_path):
        realPath = topUsers2_path + filename
        with open(realPath, 'rb') as csvfile:
            # each file is a user
            csvreader = csv.reader(csvfile, delimiter=',')

            user_heard = Set([])
            songid_hex_map = {}

            userHex = ''
            songHex = ''
            tripleHex = ''

            for i, row in enumerate(csvreader):
                if i != 0:
                    if i == 1:
                        new_name = names.get_first_name()
                        while new_name in used_names:
                          new_name = names.get_first_name()
                        used_names.add(new_name)
                        userHex = ''.join([random.choice(string.hexdigits + string.digits) for n in xrange(24)])
                        users.append({'_id': userHex, 'username': new_name, 'idString': userId, 'password': 'brown123', 'provider': 'local'})

                    userId = row[0]
                    songId = row[1] 
                    songPlayCount = int(row[2])
                    songTitle = row[4]
                    songAuthor = row[9]

                    if songId in song_index_map:
                    
                        # Triple already exists, just add to it.
                        if songId in user_heard:
                    
                            currSongHex = songid_hex_map[songId]
                        
                            currTriple = findTriple(userHex, songHex, triples)
                            oldCount = triples[currTriple].count
                            #triples[currTriple] = {user: userHex, song: songHex, count: (songPlayCount+oldCount)}

                            print "No debe llegar aqui nunca!!!!"
                            exit(1)
                            
                    	
                    else: 
                        songHex = ''.join([random.choice(string.hexdigits + string.digits) for n in xrange(24)])
                        songs.append({'_id': songHex, 'idString': songId, 'author': songAuthor, 'title': songTitle})
                    
                        tripleHex = ''.join([random.choice(string.hexdigits + string.digits) for n in xrange(24)])
                        triples.append({'user': userHex, 'song': songHex, 'songTitle': songTitle, 'songAuthor': songAuthor, 'count': songPlayCount})
                    
                        song_index_map[songId] = songHex

                    user_heard.add(songId)
                    

    songfile = open('Song.json', 'w')
    json.dump([{'model': 'Song', 'documents': songs}], songfile);
    songfile.close();

    userfile = open('User.json', 'w')
    json.dump([{'model': 'User', 'documents': users}], userfile);
    userfile.close();

    triplefile = open('Triple.json', 'w')
    json.dump([{'model': 'Triple', 'documents': triples}], triplefile);
    triplefile.close();

def main():
    print "generating json"

    getUserInterestMatrix()

    print "done"


if __name__ == '__main__':
    main()
