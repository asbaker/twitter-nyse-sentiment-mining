require 'twitter'
require 'pry'
require 'mongoid'

require './tweet'

p "**************************************************"

Mongoid.load!('mongoid.yml', :development)

client = Twitter::REST::Client.new do |config|
  config.consumer_key    = ENV['TWITTER_KEY']
  config.consumer_secret = ENV['TWITTER_SECRET']
end

config = Constants.first || Constants.new({last_tweet_id: 1})
puts "Last tweet id #{config.last_tweet_id}"

HOW_MANY = 100

puts "Fetching #{HOW_MANY} tweets"

count = 1
client.search("#nyse",
              result_type: "recent",
              count: HOW_MANY,
              lang: 'en', since_id: config.last_tweet_id).take(HOW_MANY).each do |tweet|

  puts "processing tweet #{count}"

  user_doc = User.new
  user_doc.twitter_id = tweet.user.id
  user_doc.name = tweet.user.name
  user_doc.lang = tweet.user.lang
  user_doc.statuses_count = tweet.user.statuses_count
  user_doc.favorites_count = tweet.user.favorites_count
  user_doc.followers_count = tweet.user.followers_count
  user_doc.friends_count = tweet.user.friends_count
  user_doc.twitter_created_at = tweet.user.created_at

  tweet_doc = Tweet.new
  tweet_doc.twitter_id = tweet.id
  tweet_doc.text = tweet.text
  tweet_doc.lang = tweet.lang
  tweet_doc.favorite_count = tweet.favorite_count
  tweet_doc.retweet_count = tweet.retweet_count
  tweet_doc.twitter_created_at = tweet.created_at
  tweet_doc.user = user_doc
  tweet_doc.save

  if config.last_tweet_id < tweet.id
    config.last_tweet_id = tweet.id
    config.save
    puts "updating last tweet id"
  end
  count = count.next
end

puts "Done"
p "**************************************************"
