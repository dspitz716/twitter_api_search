# twitter_api_search
find tweets containing a user specified string

##main functions
###goop_tweets()
using the tweepy library make a call to the twitter api and pull 500 tweets, add these tweets to a list and create a timestamped json file containing the tweets
###process_data()
combine all json files in the twitter_json directory and perform some transformations on the data to create a single dataframe that will write to a csv file in the twitter_csv directory
