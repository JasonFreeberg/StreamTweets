# Jason Freeberg
# August 18th 2016
# Stream and store Tweets for projects!
# persistwifi() reconnects wifi and exponentially backs off
# Tweets are thrown into a local MongoDB database

import sys
import subprocess
import tweepy as tp
import time
from WiFi import persistConnection
from Queue import Queue
from pymongo import MongoClient, errors
from tweepy.utils import import_simplejson
from tweepy.models import Status
from httplib import IncompleteRead

with open(sys.argv[1], 'r') as f:
    args = f.readlines()

args = [item.strip('\n') for item in args]

# Twitter keys and tokens
# You can make the stream time and keywords as command line arguments using "sys.argv([2])" and so on
# Or take them from the text file using "args[7]" and so on
KEY = args[0]
SECRET = args[1]
ACCESS_TOKEN = args[2]
ACCESS_SECRET = args[3]
# Database names and locations
DATABASE_NAME = args[4]
COLLECTION_NAME = args[5]
DATA_LOCATION = args[6]
STREAM_TIME = 45  # in seconds
KEYWORDS = ['Trump']

# Read text file with tokens and collections

class MyStreamListener(tp.StreamListener):
    """
    Overwrite portion of tweepy.StreamListener class
    Change the class's method when data is streamed through object
    """

    def __init__(self, a_collection=None):
        tp.StreamListener.__init__(self)
        self.collection = a_collection
        self.collection_ids = []
        self.json = import_simplejson()

    def on_data(self, raw_data):
        """
        Called when raw data is received from connection.
        Coerce to json, print id, insert to mongodb.
        """
        data = self.json.loads(raw_data)

        try:
            data[u'_id'] = data.pop(u'id')
            self.collection.insert_one(data)
            self.collection_ids.append(data[u'_id'])
            print data[u'text']
            if self.collection.count() % 10 is 0:
                print '#####', 'N records =', self.collection.count()
        except errors.DuplicateKeyError as noprint:
            pass
        except AttributeError as ex:
            print '#####', 'ERROR: Did you assign a mongo collection to this MyStreamListener object?'
            print '#####', 'Message:', ex.message
            raise
        except Exception as ex:
            print '#####', 'WARN:', ex.message
        return True

# Database instantiation and connection
subprocess.Popen(['mongod', '--dbpath', DATA_LOCATION])
client = MongoClient('localhost', 27017)
myCollection = client[DATABASE_NAME][COLLECTION_NAME]

# API authorization and setup
auth = tp.OAuthHandler(KEY, SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tp.API(auth)

# Instantiate an edited listener object
# Add the mongodb collection to the stream object
editedListener = MyStreamListener(a_collection=myCollection)

now = time.time()
stop_time = now + STREAM_TIME

# And begin streaming!
print '#############################'
print 'Stream for', STREAM_TIME, 'seconds.'
print '#############################', '\n'

# Remove the while loop if you do not want the script to persist
# the WiFi connection. Remember to set a STREAM_TIME if you do so.
# To slow the stream of Tweets, at a time.sleep() in the edited stream
# listener earlier in this script.
while persistConnection():
    try:
        myStream = tp.Stream(auth=api.auth,
                             listener=editedListener)
        myStream.filter(track=KEYWORDS,
                        languages=['nl'],
                        stall_warnings=True,
                        async=True)
    # Not a graceful handling; works but could be improved upon.
    except IncompleteRead as noprint:
        print 'read wrong'
        continue
    except KeyboardInterrupt:
        break

# Summary output
print '#####', 'Disconnecting...'
time.sleep(STREAM_TIME)
myStream.disconnect()
del myStream

print '\n', '#############################'
print 'Stream disconnected.'
print '#############################', '\n'

# Check for duplicate _ids in data entering collection
Nset = len(set(editedListener.collection_ids))
Nlist = len(editedListener.collection_ids)

if Nset == Nlist:
    print 'Correct number of unique ids (%s).' % Nset
    print myCollection.count(), 'Records in collection'
    print 'Collection is %s MB.' % (myCollection.__sizeof__())
    print "Congratulations, you didn't fuck up!"
else:
    print "WARN: Incorrect number of unique ids; id key may have duplicates."
    print 'Unique =', Nset
    print 'Total =', Nlist

sys.exit(101)
