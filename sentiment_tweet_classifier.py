from __future__ import division
import nltk, re, pprint
from nltk import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.stem.porter import *

stemmer = PorterStemmer()

def stem(word):
  return stemmer.stem(word)
  #return word

def features(word):
  return {'word': word}

def filtered_word(word):
  isStopword = word in stopwords.words('english')
  excluded = word in ['seas', '&', 'amp', '$', '#', '``', ':', "//", "http", "@", "...", "''", "(", ")", "tsx", "oil"] or word.find("t.c") != -1 or word.find("-star") != -1
  return isStopword or excluded

def get_tweets(filename, sentiment):

  tweets = []
  f = open(filename)
  for line in f.readlines():
    clean_line = re.sub(r'\W+ ', '', line.lower())
    words = word_tokenize(clean_line)
    tweet = [stem(w) for w in words if not filtered_word(w)]
    tweets.append( (tweet, sentiment) )

  return tweets

def get_words_in_tweets(tweets):
  all_words = []
  for (words, sentiment) in tweets:
    all_words.extend(words)
  return all_words

def get_word_features(wordlist):
  wordlist = nltk.FreqDist(wordlist)
  word_features = wordlist.keys()
  return word_features

def extract_features(document):
  document_words = set(document)
  features = {}
  for word in word_features:
    features['contains(%s)' % word] = (stem(word) in document_words)
  return features


pos_tweets = get_tweets('data/tweet_pos.csv', 'pos')
neg_tweets = get_tweets('data/tweet_neg.csv', 'neg')
tweets = pos_tweets + neg_tweets

posco = int(len(pos_tweets)*3/4)
negco = int(len(neg_tweets)*3/4)

train_tweets = pos_tweets[:posco] + neg_tweets[:negco]
test_tweets = pos_tweets[posco:] + neg_tweets[negco:]

print 'train on %d instances, test on %d instances' % (len(train_tweets), len(test_tweets))

word_features = get_word_features(get_words_in_tweets(train_tweets))
training_set = nltk.classify.apply_features(extract_features, train_tweets)
testing_set = nltk.classify.apply_features(extract_features, test_tweets)

classifier = NaiveBayesClassifier.train(training_set)
classifier.show_most_informative_features()

print 'accuracy:', nltk.classify.util.accuracy(classifier, testing_set)


example_tweets = [
  "Tencent Is Becoming A Global Entertainment Power, to compete with AliBaba for content http://t.co/aGPB46rdjX $BABA $LGF $TWX #Stocks #NYSE",
  "3-star analyst Bhavan Suri from William Blair reiterated a BUY on $VEEV. Bhavan has a 67% success rate http://goo.gl/i729x6  #NYSE #stocks",
  "0-star analyst Philip Shen from Roth Capital maintained a HOLD on $SOL. Philip has a 34% success rate http://goo.gl/ktYtpY  #NYSE #stocks",
  "2-star analyst James Kisner from Jefferies reiterated a HOLD on $HPQ.  http://goo.gl/Os1Wiy  #NYSE #stocks #HPQ",
  "1-star analyst Judson Bailey from Wells Fargo maintained a SELL on $SDRL. Judson has a 22.2% success rate http://goo.gl/rvdT6T  #NYSE",
  "Halliburton and Macy's Big Market Movers http://cur.lv/g0rtv  #NYSE",
  "Movers and Shakers: Recently Upgraded: $NADL $SO $SDRL $SPLS $AAL $HES $GLNG $MXIM $BDX $BLOX $KKR $QIHU $SCTY $TJX $PBR #trading #nyse",
  "United Airlines providing entertainment content to your Android device during flights http://bit.ly/1xkcQGM  #DownloadLink #NYSE #UAL",
  "Yahoo May Become The Better Play On Search http://seekingalpha.com/article/2715605-yahoo-may-become-the-better-play-on-search?source=feed_f $AAPL #APPLE $GOOG $MSFT $GOOGL $YHOO",
  "See why $FB, $GOOG & $TWTR are faves in my charitable trust. http://www.go-tst.com/EFa7g "
]


for tweet in example_tweets:
  c = classifier.prob_classify(extract_features(tweet.split()))

  print '*'*80
  print 'tweet:', tweet
  print 'probability positive: ', c.prob('pos')
  print 'probability negative: ', c.prob('neg')
  print '*'*80


