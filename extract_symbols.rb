require 'pry'
require 'mongoid'

require './tweet'

Mongoid.load!('mongoid.yml', :development)


symbol_regex = /\$[a-fA-f]{3,4}/

Tweet.all.each do |tweet|
  tweet.symbols = tweet.text.scan(symbol_regex)
  tweet.save

  p tweet.symbols
end
