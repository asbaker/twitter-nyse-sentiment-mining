from pymongo import MongoClient
from datetime import datetime
from pytz import timezone
import csv

client = MongoClient()
db = client.twitter
tweets = db.tweets

eastern = timezone('US/Eastern')
day_start = eastern.localize(datetime(2014,11,1,10,0))
day_end = eastern.localize(datetime(2014,11,28,14,0))

print "Total Tweets --- %s" % tweets.count()

res = tweets.find({"twitter_created_at": {"$gte": day_start, "$lt": day_end}})

with open("data/tweets.csv", 'wb') as csvfile:
  w = csv.writer(csvfile)
  for tweet in res:
    w.writerow([tweet['text'].encode('ascii', 'ignore')])
