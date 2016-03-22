import os
import sys
import glob
import time
import datetime
import numpy as np
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

    print "artists are: "
    print artists

    print "artist artist_hottness are: "
    print artist_hottness

    print "artist_familiarity are: "
    print artist_familiarity


    closeDBConnection()


    

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
    print '* one artist having familiaryt >0.8:'

    return res.fetchall()



if __name__ == '__main__':
    # if len(sys.argv) < 4:
    #     print 'Usage: python process.py pinterest furniture_names stopwords'
    # pinterest_path = sys.argv[1]
    # furniture_names_path = sys.argv[2]
    # stopwords_path = sys.argv[3]
    main()

