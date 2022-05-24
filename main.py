import os
import glob
import pandas as pd
import datetime
from datetime import datetime
import json
import tweepy


def goop_tweets(api, timestamp):
    # this call brings in the entire search_tweets object (I believe having more data upfront is better if possible). the json file generated will contain 500 items
    goop = tweepy.Cursor(api.search_tweets, q='goop', count=100).items(500)
    data = []
    for tweet in goop:
        item = tweet._json
        data.append(item)
    jsonData = json.dumps(data)
    with open(f'twitter_json/tweets_{timestamp}.json', 'w') as outfile:
        json.dump(jsonData, outfile)


def process_data(timestamp, filepath, filepath_csv):

    json_pattern = os.path.join(filepath, '*.json')
    csv_pattern = os.path.join(filepath_csv, '*.csv')
    file_list = glob.glob(json_pattern)

    # read all files in the twitter_json directory and iterate through each to create 1 dataframe with all the data
    dfs = []
    for file in file_list:
        with open(file, 'r') as f:
            json_data = json.load(f)
            df = pd.read_json(json_data)
            df = df.rename(columns={'created_at': 'tweet_created_at'})
            df = df[['tweet_created_at', 'text', 'user']]
            df1 = pd.concat([df, pd.json_normalize(df['user'])], axis=1)
            df2 = df1[['tweet_created_at', 'text', 'location', 'followers_count']]
        dfs.append(df2)
    df = pd.concat(dfs)

    # get total number of files found
    num_files = len(dfs)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(dfs, 1):
        print('{}/{} files processed.'.format(i, num_files))

    csv_list = glob.glob(csv_pattern)
    #you can use this small block to delete all of the csv files in the directory if you wanted to
    #for f in csv_list:
        #os.remove(f)
    #convert df to csv
    df.to_csv(f'twitter_csv/tweets_{timestamp}.csv')


def main():
    auth = tweepy.OAuth2AppHandler('ptjPfTgqLUSpz7bKKfo1G9zw9', 'Q03zJ1DUY1GViDfHCGTzKpsc6kgkA7P06Z59fzYo5LMxTK3Hiy')
    api = tweepy.API(auth, wait_on_rate_limit=True)
    timestamp = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
    goop_tweets(api, timestamp)
    process_data(timestamp, filepath='twitter_json', filepath_csv='twitter_csv')


if __name__ == '__main__':
    main()