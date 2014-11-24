require 'mongoid'

class Tweet
  include Mongoid::Document

  field :twitter_id, type: Integer
  field :text, type: String
  field :lang, type: String
  field :favorite_count, type: Integer
  field :retweet_count, type: Integer
  field :twitter_created_at, type: DateTime
  embeds_one :user
end

class User
  include Mongoid::Document

  field :twitter_id, type: Integer
  field :name, type: String
  field :lang, type: String
  field :statuses_count, type: Integer
  field :favorites_count, type: Integer
  field :followers_count, type: Integer
  field :friends_count, type: Integer
  field :twitter_created_at, type: DateTime
end

class Constants
  include Mongoid::Document

  field :last_tweet_id, type: Integer
end

