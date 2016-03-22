#!/usr/bin/env python
import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import os
import sys
import csv
import glob
import time
import datetime
try:
    import sqlite3
except ImportError:
    print 'you need sqlite3 installed to use this program'
    sys.exit(0)


# PATH TO track_metadat.db
# CHANGE THIS TO YOUR LOCAL CONFIGURATION
# IT SHOULD BE IN THE ADDITIONAL FILES
# (you can use 'subset_track_metadata.db')
dbfile = 'data/subset_track_metadata.db'

# connect to the SQLite database
conn = sqlite3.connect(dbfile)

# from that connection, get a cursor to do queries
c = conn.cursor()

# so there is no confusion, the table name is 'songs'
TABLENAME = 'songs'


def main():
    arrTuples = getArtistHotness()

    artists, artist_hottness, artist_familiarity = zip(*arrTuples)

    # print "artists are: "
    # print list(artists)

    # print "artist_hottness are: "
    # print list(artist_hottness)

    # print "artist_familiarity are: "
    # print list(artist_familiarity)

    closeDBConnection()

    """calculate and plotting K means and with cluster point scatter vs. K"""
    input_data, labels = setup(arrTuples)
    print "Input Data:"
    print input_data
    print  
    N = len(input_data)
    min_with_cluster_point_scatter = float("inf")
    for x in range(15):
        within_cluster_point_scatter, new_means, new_cluster_array = calculate_within_cluster_point_scatter_and_mean(3,N,input_data)
        if within_cluster_point_scatter < min_with_cluster_point_scatter:
            min_with_cluster_point_scatter = within_cluster_point_scatter
            means = new_means
            cluster_array = new_cluster_array
    print "labels assigned to clusters:"
    print zip(labels, cluster_array)
    print
    print "K means:"
    print means
    print

    header = ["artist_name", "cluster", "hotness", "familiarity"]
    
    with open('artist_cluster.csv', 'wb') as f:
        writer = csv.writer(f)
        # Write CSV Header, If you dont need that, remove this line
        writer.writerow(header)
        allZip =  zip(labels, cluster_array, input_data)

        for label, cluster, input_d in allZip:
            writer.writerow([label.encode("utf-8"), cluster, input_d[0], input_d[1]])



    kmeans_coordinates =  ["x_value", "y_value"]

    with open('kmeans_coordinates.csv', 'wb') as f:
        writer = csv.writer(f)
        # Write CSV Header, If you dont need that, remove this line
        writer.writerow(kmeans_coordinates)

        for m in means:
            writer.writerow([m[0], m[1]])
        

        #for artist in allZip:
         #   writer.writerow([])


    #plot_kmeans(plt,input_data,means,countries, cluster_array)
    #plot_and_calculate_within_cluster_point_scatter(plt, N, input_data)

    

def closeDBConnection():
    # close the cursor and the connection
    # (if for some reason you added stuff to the db or alter
    #  a table, you need to also do a conn.commit())
    c.close()
    conn.close()

def encode_string(s):
    """
    Simple utility function to make sure a string is proper
    to be used in a SQLite query
    (different than posgtresql, no N to specify unicode)
    EXAMPLE:
      That's my boy! -> 'That''s my boy!'
    """
    return "'"+s.replace("'","''")+"'"

def getArtistHotness():
    # get all artists whose artist familiarity is > .8
    q = "SELECT DISTINCT artist_name, artist_familiarity, artist_hotttnesss FROM songs WHERE artist_familiarity>0 AND artist_hotttnesss>0"
    res = c.execute(q)

    return res.fetchall()




def setup(arrTuples):
    labels = [] 
    inputs = []

    for  artist, hotness, familiarity in arrTuples:
        inputs.append((float(hotness),float(familiarity)))
        labels.append(artist)

    labels = np.array(labels) 
    inputs = np.array(inputs)
    return (inputs, labels)

def square_distance(A, B): 
    """(a_1 - b_1) ** 2 + ... + (a_n - b_n) ** 2"""
    return np.sum((A-B)**2)

def determine_closest_centroid(input, means,K):
    """return the index of the cluster closest to the input"""
    min_distance = float("inf")
    for i in range(K):
        distance = square_distance(input, means[i])
        if distance < min_distance:
            min_distance = distance
            index = i
    return index  

def k_means(K,inputs):
    """calculate K means until completion"""
    N = len(inputs)
    aXmeans_byCluster = np.random.rand(K, inputs.shape[1]) * (np.max(inputs, axis=0) - 
    np.min(inputs, axis=0)) + np.min(inputs, axis=0) 
    aiCluster = np.zeros(N, int)

    while True:
        new_aiCluster = np.zeros(N, int)
        for i in range(N):
            new_aiCluster[i] = determine_closest_centroid(inputs[i], aXmeans_byCluster, K)

        if np.array_equal(aiCluster,new_aiCluster):               
            return (aXmeans_byCluster, aiCluster) 

        aiCluster = new_aiCluster 
        for i in range(K): 
            points = np.array([p for p, a in zip(inputs, aiCluster) if a == i])           
            if points.size != 0:                                
                aXmeans_byCluster[i] = np.mean(points, axis = 0)  
    
def plot_kmeans(plt, inputs, cluster_means, countries_label,cluster_array_data):
    """ plot K means graphically for K = 3 with colors"""
    x_means = []
    y_means = []
    for ele in cluster_means:
        x_means.append(ele[0])
        y_means.append(ele[1])
    plt.scatter(x_means[0], y_means[0], s = 500, c = 'red')
    plt.scatter(x_means[1], y_means[1], s = 500, c = 'green')
    plt.scatter(x_means[2], y_means[2], s = 500, c = 'blue')
    x_data = []
    y_data = []
    for ele in inputs:
        x_data.append(ele[0])
        y_data.append(ele[1])
    for i, k in enumerate(cluster_array_data):
        if k == 0:
            plt.scatter(x_data[i],y_data[i], color = 'red')
        if k == 1:
            plt.scatter(x_data[i],y_data[i], color = 'green')
        if k == 2:
            plt.scatter(x_data[i],y_data[i], color = 'blue')
  
    for label, x_count, y_count, k in zip(countries_label, x_data, y_data, 
                                        cluster_array_data):
        if k == 0:
            plt.annotate(label,
                xy=(x_count,y_count),
                xytext=(5,-5),
                textcoords = 'offset points',
                color = 'red')
        if k == 1:
            plt.annotate(label,
                xy=(x_count,y_count),
                xytext=(5,-5),
                textcoords = 'offset points',
                color = 'green')
        if k == 2:
            plt.annotate(label,
                xy=(x_count,y_count),
                xytext=(5,-5),
                textcoords = 'offset points',
                color = 'blue')
    plt.title("White Meat vs. Red Meat with K = 3")
    plt.xlabel("Red Meat")
    plt.ylabel("White Meat")
    plt.show()

def calculate_within_cluster_point_scatter_and_mean(K, N, inputs):
    """calculate within cluster point scatter"""
    assigned_clusters = np.zeros(N, int)
    means, assigned_clusters = k_means(K,inputs)
    sum_of_within_cluster_squared_distances = 0
    for input, a in zip(inputs, assigned_clusters):
        sum_of_within_cluster_squared_distances += square_distance(input, means[a])
    return (sum_of_within_cluster_squared_distances, means, assigned_clusters)

def plot_and_calculate_within_cluster_point_scatter(plt, N, inputs):
    """plot within cluster point scatter vs. K"""
    ks = range(1, 20)
    scatters = []
    for k in ks:
        min_with_cluster_point_scatter = float("inf")
        for x in range(1):
            within_cluster_point_scatter, _, _ = calculate_within_cluster_point_scatter_and_mean(k,N,inputs)
            if within_cluster_point_scatter < min_with_cluster_point_scatter:
                min_within_cluster_point_scatter = within_cluster_point_scatter
        scatters.append(min_within_cluster_point_scatter)
    plt.plot(ks, scatters)
    plt.xticks(ks)
    plt.title("Within Cluster Point Scatter vs. K")
    plt.xlabel("k")
    plt.ylabel("within cluster point scatter")
    plt.show()

if __name__ == '__main__':
    # if len(sys.argv) < 4:
    #     print 'Usage: python process.py pinterest furniture_names stopwords'
    # pinterest_path = sys.argv[1]
    # furniture_names_path = sys.argv[2]
    # stopwords_path = sys.argv[3]
    main()

