# -*- coding: utf-8 -*-
"""
Original file is located at
    https://colab.research.google.com/drive/1KsysvpbMcXdmBai8QTBZfDltrPtLYW30
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections
import nltk
from nltk.corpus import stopwords
import re
import sqlite3

import warnings
warnings.filterwarnings("ignore")

sns.set(font_scale=1.5)
sns.set_style("whitegrid")


def extract_data(uni_name):

    #Extract twitter data from database and store it in pandas dataframe
    conn = sqlite3.connect('twitter.sqlite')
    df = pd.read_sql("select * from Tweets",conn)
    conn.commit()
    conn.close()

    #df = pd.read_csv("dataset/tweets.csv")
    df = df[df["University"] == uni_name]
    df_tweets = pd.DataFrame().assign(Tweet=df['Tweet'])
    #print(df.head(1))

    df_tweets.size

    """### Remove URLs (links)"""

    def remove_url(txt):
        """Replace URLs found in a text string with nothing 
        (i.e. it will remove the URL from the string).

        Parameters
        ----------
        txt : string
            A text string that you want to parse and remove urls.

        Returns
        -------
        The same txt string with url's removed.
        """

        return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

    all_tweets_no_urls = [remove_url(tweet) for tweet in df_tweets.Tweet]
    all_tweets_no_urls[:5]

    """### Text Cleanup - Address Case Issues"""

    # Create a list of lists containing lowercase words for each tweet
    words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]

    """### Calculate and Plot Word Frequency"""

    # List of all words across tweets
    all_words_no_urls = list(itertools.chain(*words_in_tweet))

    # Create counter
    counts_no_urls = collections.Counter(all_words_no_urls)

    """### Remove Stopwords With nltk"""

    nltk.download('stopwords')

    stop_words = set(stopwords.words('english'))
    # Remove stop words from each tweet list of words
    tweets_nsw1 = [[word for word in tweet_words if not word in stop_words]
                for tweet_words in words_in_tweet]


    tweets_nsw = [[word for word in sentence if len(word) >= 4] for sentence in tweets_nsw1 ]

    tweets_nsw

    """### Remove Collection Words"""

    def flatten(l):
        return [item for sublist in l for item in sublist]

    uni_list = df.University.tolist()
    uni_list = list(set(uni_list))
    uni_list = [x.lower() for x in uni_list]
    # using list comprehension + split()
    # Tokenizing strings in list of strings
    res = [sub.split() for sub in uni_list]
    #convert list of list to list
    list_text = flatten(res)
    list_text = list(set(list_text))
    tweets_nsw_nc = [[w for w in word if not w in list_text]
                    for word in tweets_nsw]

    """### Calculate and Plot Word Frequency of Clean Tweets"""

    # Flatten list of words in clean tweets
    all_words_nsw_nc = list(itertools.chain(*tweets_nsw_nc))

    # Create counter of words in clean tweets
    counts_nsw_nc = collections.Counter(all_words_nsw_nc)
    
    clean_tweets_ncw = pd.DataFrame(counts_nsw_nc.most_common(15),
                                columns=['words', 'count'])
    print(clean_tweets_ncw)
    return clean_tweets_ncw
    
    #fig, ax = plt.subplots(figsize=(8, 8))

    # Plot horizontal bar graph
    #clean_tweets_ncw.sort_values(by='count').plot.barh(x='words',
                       # y='count',
                       # ax=ax,
                       # color="purple")

    #ax.set_title("Common Words Found in Tweets (Without Stop or Collection Words)")
    
    #plt.show()

extract_data("Massachusetts Institute of Technology (MIT)")


def top_tweets(uni_name):
    #Extract twitter data from database and store it in pandas dataframe
    conn = sqlite3.connect('twitter.sqlite')
    df1 = pd.read_sql("select * from Tweets",conn)
    conn.commit()
    conn.close()

    df1 = df1[df1["University"] == uni_name]
    df_top = df1.nlargest(5, "Retweets")
    #print(df_top.head())

top_tweets("Australian National University (ANU)")
    