from pymongo import MongoClient
from datetime import datetime
from pytz import timezone
from scipy.stats import itemfreq
import numpy as np

client = MongoClient()
db = client.twitter
tweets = db.tweets

eastern = timezone('US/Eastern')
day_start = eastern.localize(datetime(2014,11,24,16,0))
day_end = eastern.localize(datetime(2014,11,25,16,0))

## (u'$PANW', 10), (u'$QQQ', 13), (u'$AAPL', 16), (u'$VSR', 16), (u'$TWTR', 27)



print "Total Tweets --- %s" % tweets.count()

res = tweets.find({"twitter_created_at": {"$gte": day_start, "$lt": day_end}})

print "Tweets between %s and %s --- %s", day_start, day_end, res.count()

#flat map
all_symbols = sum(map(lambda t: t['symbols'], res), [])

# get a frequency list
items, inv = np.unique(all_symbols, return_inverse=True)
freq = np.bincount(inv)
symbol_freq = zip(items, freq)

print sorted(symbol_freq, key=lambda x: x[1])

