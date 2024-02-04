import snscrape.modules.twitter as sntwitter
import pandas as pd
import sqlite3

# Creating list to append tweet data to
attributes_container = []
def tweet_scrape(query):
    

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i > 500:
            break
        attributes_container.append(
            [tweet.user.username, tweet.url, tweet.retweetCount, tweet.content, query])

    # Creating a dataframe to load the list
    tweets_df = pd.DataFrame(attributes_container, columns=[
                             "User", "URL", "Retweets", "Tweet", "University"])
    #tweets_df["university"] = query
    tweets_df.to_csv('dataset/tweets.csv', index=False)


#Extract university names from rankings database in order to extract tweets
conn = sqlite3.connect('twitter.sqlite')
df_ranking = pd.read_sql("select * from Ranking",conn)
conn.commit()
conn.close()

list_text = df_ranking.name.tolist()

for i in range(len(list_text)):

    search = list_text[i]
    tweet_scrape(search)


#Add twitter data to database
df = pd.read_csv('dataset/tweets.csv')
table_name = 'Tweets'
conn = sqlite3.connect('twitter.sqlite')
query = f'Create table if not Exists {table_name} (User text, URL text, Retweets real, Tweet text, University text)'
conn.execute(query)
df.to_sql(table_name,conn,if_exists='replace',index=False)
conn.commit()
conn.close()