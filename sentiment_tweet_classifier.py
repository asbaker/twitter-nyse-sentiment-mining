from __future__ import division
#import nltk.classify.util
import nltk, re, pprint
from nltk import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords

def features(word):
  return {'word': word}

def filtered_word(word):
  isStopword = word in stopwords.words('english')
  excluded = word in ['$', '&', 'amp', '@', ';', ':', '#', 'http', '!', '/', '``', "''", ",", ".", "...", "--"] or word.find("t.co") != -1
  return isStopword or excluded


def get_tweets(filename, sentiment):
  tweets = []
  f = open(filename)
  for line in f.readlines():
    words = word_tokenize(line.lower())
    tweet = [w for w in words if not filtered_word(w)]
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
    features['contains(%s)' % word] = (word in document_words)
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

