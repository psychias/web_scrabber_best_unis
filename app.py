import streamlit as st
import os
import joblib
import sqlite3
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import streamlit.components.v1 as components
import requests
import students
from freq_words import *
import freq
select = ""


def main_q():

    col1, col2, col3 = st.columns(3)
    menu = ["Search"]
    st.sidebar.header("Menu")

    df = pd.read_csv('dataset/rankings.csv', encoding="ISO-8859-1")
    uni_list = list(df['name'])
    uni_rank = df['rank']
    col_names = list(df.columns)

    menu = ["Home", "Universities"]
    name_rank = ["By Name", "By Rank"]
    choice = st.sidebar.selectbox("", menu)
    if choice == "Home":
        col2.title("Top 30 Universities \n")
        st.subheader("Home")
        ch = st.selectbox("Options", name_rank)
        if ch == "By Name":
            select = st.selectbox("Choose university By Name", uni_list)
            st.write("Selected University Information", df[df.name == select])
            top_tweets_by_name(select)

        elif ch == "By Rank":
            select_rank = st.selectbox("Choose university By Rank", uni_rank)
            st.write("Selected University Information",
                     df[uni_rank == select_rank])
            top_tweets_by_rank(select_rank, df)

    elif choice == "Universities":
        col2.title("Top 30 Universities \n")
        st.subheader("Universities List")
        # for i in df:
        university_data(df)



def the_Tweet(tweet_url):
    # We will use f-strings for string interpolation
    for i in tweet_url:
        api = "https://publish.twitter.com/oembed?url={}".format(i)
        response = requests.get(api)
    #res = response.json()
        res = response.json()["html"]
        components.html(res, height=500, scrolling=True)

    # Implementing Streamlit Syntax


def university_data(data):
    # AgGrid(data)
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
    gb.configure_side_bar()  # Add a sidebar
    # Enable multi-row selection
    gb.configure_selection('multiple', use_checkbox=True,
                           groupSelectsChildren="Group checkbox select children")
    gridOptions = gb.build()

    AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        theme='alpine',  # Add theme color to thse table
        enable_enterprise_modules=True,
        height=1360,
        width='90%',
        reload_data=True
    )


def top_tweets_by_name(uni_name):
    # Extract twitter data from database and store it in pandas dataframe
    conn = sqlite3.connect('twitter.sqlite')
    df1 = pd.read_sql("select * from Tweets", conn)
    conn.commit()
    conn.close()

    df1 = df1[df1["University"] == uni_name]
    df_top = df1.nlargest(5, "Retweets")
    url_list = list(df_top["URL"])
    tw = url_list
    #the_Tweet(tw)
    #return tw
    PAGES = {
        "Students",
        "Frequent Words",
        "Tweets" ,
    }
    selection = st.radio("Choose to go to page", list(PAGES))
    if selection == "Tweets":
        st.write("Top 5 Tweets: ")
        the_Tweet(tw)
        #page.app_show(tw)
    elif selection == "Students":
        page = students
        page.app(uni_name)
    elif selection == "Frequent Words":
        page = freq
        page.app(uni_name)
    


# st.write(url_list)


def top_tweets_by_rank(uni_rank, df):
    # Extract twitter data from database and store it in pandas dataframe
    conn = sqlite3.connect('twitter.sqlite')
    df1 = pd.read_sql("select * from Tweets", conn)
    conn.commit()
    conn.close()

    uni_name = df.loc[df["rank"] == uni_rank, "name"].iloc[0]
    df1 = df1[df1["University"] == uni_name]
    df_top = df1.nlargest(5, "Retweets")
    url_list = list(df_top["URL"])
    tw = url_list
    PAGES = {
        "Students",
        "Frequent Words",
        "Tweets" ,
    }
    selection = st.radio("Choose to go to page", list(PAGES))
    if selection == "Tweets":
        st.write("Top 5 Tweets: ")
        the_Tweet(tw)
        #page.app_show(tw)
    elif selection == "Students":
        page = students
        page.app(uni_name)
    elif selection == "Frequent Words":
        page = freq
        page.app(uni_name)
    # st.write(url_list)


if __name__ == '__main__':
    main_q()
    # top_tweets(a)
