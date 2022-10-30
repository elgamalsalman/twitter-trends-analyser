import os
import sys
import json
import tweepy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import numpy as np
import datetime as dt
from dotenv import load_dotenv

MAX_TICKER_COUNT = 15

# ---------- FUNCTIONS ----------
def get_twitter_client():
	# load environment
	load_dotenv()

	# authentication
	consumer_key = os.getenv('API_KEY')
	consumer_secret = os.getenv('API_KEY_SECRET')
	access_token = os.getenv('ACCESS_TOKEN')
	access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
	bearer_token = os.getenv('BEARER_TOKEN')

	return tweepy.Client(
		bearer_token,
		consumer_key, 
		consumer_secret, 
		access_token, 
		access_token_secret
	)

# ------------ MAIN ------------
if __name__ == '__main__':
	# create the twitter client
	twitter = get_twitter_client()

  # take the input
	query = input('input the keywords to look for seperated by spaces: ')
	start_time = input('input the start time (YYYY-MM-DD): ')
	file_name = input('input the name of the file to save the plot to: ')

	# start from the start of the day
	start_time += 'T00:00:00.000Z'

	# get the twitter count data from the twitter API
	responce = twitter.get_recent_tweets_count(query=query, granularity='day', start_time=start_time).data[:-1]
	days_count = len(responce)

	# form a list of only the tweet counts
	y = [res['tweet_count'] for res in responce]
	
	# range dates
	end = dt.datetime.now().date()
	start = end - dt.timedelta(days_count)
	x = mdates.drange(start, end, dt.timedelta(days=1))

	# create the plot
	plt.title(query)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
	plt.gca().xaxis.set_major_locator(MaxNLocator(min(MAX_TICKER_COUNT, days_count)))
	plt.plot(x,y)
	plt.gcf().autofmt_xdate()
	plt.savefig(file_name)
	plt.show()