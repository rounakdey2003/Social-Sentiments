import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

from modules.facebook_analyzer import FacebookAnalyzer
from modules.instagram_analyzer import InstagramAnalyzer
from modules.instagram_alternative import InstagramAlternativeAnalyzer
from modules.twitter_analyzer import TwitterAnalyzer
from modules.reddit_analyzer import RedditAnalyzer
from modules.sentiment_engine import SentimentEngine

st.set_page_config(
    page_title="Social Media Sentiment Analyzer",
    page_icon="📊",
    layout="centered"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.dialog("Facebook Configuration")
def show_facebook_dialog():
    st.write("Configure your Facebook analysis settings:")
    
    page_id = st.text_input("Facebook Page ID")
    access_token = st.text_input("Access Token", type="password")
    post_limit = st.slider("Number of posts to analyze", 10, 100, 20)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Analyze Posts", type="primary"):
            if page_id and access_token:
                st.session_state.facebook_config = {
                    'page_id': page_id,
                    'access_token': access_token,
                    'post_limit': post_limit
                }
                st.session_state.facebook_analyze = True
                st.rerun()
            else:
                st.error("Please provide Facebook Page ID and Access Token")
    
    with col2:
        if st.button("Cancel"):
            st.rerun()

@st.dialog("Instagram Configuration")
def show_instagram_dialog():
    st.write("Configure your Instagram analysis settings:")
    
    username = st.text_input("Instagram Username")
    post_limit = st.slider("Number of posts to analyze", 10, 50, 20)
    use_demo_data = st.checkbox("Use Demo Data (when rate limited)", value=False)
    
    st.info("Instagram has strict rate limits. If you encounter errors, try using demo data or wait 10-15 minutes.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Analyze Posts", type="primary"):
            if username or use_demo_data:
                st.session_state.instagram_config = {
                    'username': username,
                    'post_limit': post_limit,
                    'use_demo_data': use_demo_data
                }
                st.session_state.instagram_analyze = True
                st.rerun()
            else:
                st.error("Please provide Instagram username or enable demo data")
    
    with col2:
        if st.button("Cancel"):
            st.rerun()

@st.dialog("Twitter/X Configuration")
def show_twitter_dialog():
    st.write("Configure your Twitter/X analysis settings:")
    
    bearer_token = st.text_input("Bearer Token", type="password")
    search_query = st.text_input("Search Query (hashtag, keyword, or @username)")
    tweet_limit = st.slider("Number of tweets to analyze", 10, 100, 30)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Analyze Tweets", type="primary"):
            if bearer_token and search_query:
                st.session_state.twitter_config = {
                    'bearer_token': bearer_token,
                    'search_query': search_query,
                    'tweet_limit': tweet_limit
                }
                st.session_state.twitter_analyze = True
                st.rerun()
            else:
                st.error("Please provide Bearer Token and search query")
    
    with col2:
        if st.button("Cancel"):
            st.rerun()

@st.dialog("Reddit Configuration")
def show_reddit_dialog():
    st.write("Configure your Reddit analysis settings:")
    
    client_id = st.text_input("Client ID")
    client_secret = st.text_input("Client Secret", type="password")
    user_agent = st.text_input("User Agent", value="SentimentAnalyzer:v1.0")
    subreddit = st.text_input("Subreddit (without r/)")
    post_limit = st.slider("Number of posts to analyze", 10, 100, 25)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Analyze Posts", type="primary"):
            if client_id and client_secret and subreddit:
                st.session_state.reddit_config = {
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'user_agent': user_agent,
                    'subreddit': subreddit,
                    'post_limit': post_limit
                }
                st.session_state.reddit_analyze = True
                st.rerun()
            else:
                st.error("Please provide Reddit credentials and subreddit name")
    
    with col2:
        if st.button("Cancel"):
            st.rerun()

def main():
    st.markdown('<h1 class="main-header">Social Media Sentiment Analyzer</h1>', unsafe_allow_html=True)

    st.divider()

    platform = st.selectbox(
        "Select Social Media Platform",
        ["Select Platform", "Facebook", "Instagram", "Twitter/X", "Reddit"],
        index=0
    )

    if platform != "Select Platform":
        st.write(f"Selected: **{platform}**")
        
        if st.button(f"{platform} Analysis", type="primary"):
            if platform == "Facebook":
                show_facebook_dialog()
            elif platform == "Instagram":
                show_instagram_dialog()
            elif platform == "Twitter/X":
                show_twitter_dialog()
            elif platform == "Reddit":
                show_reddit_dialog()
    else:
        st.info("Please select a social media platform to get started with sentiment analysis.")

    st.divider()

    sentiment_engine = SentimentEngine()

    if "facebook_analyze" in st.session_state and st.session_state.facebook_analyze:
        handle_facebook_analysis(sentiment_engine)
        st.session_state.facebook_analyze = False
    elif "instagram_analyze" in st.session_state and st.session_state.instagram_analyze:
        handle_instagram_analysis(sentiment_engine)
        st.session_state.instagram_analyze = False
    elif "twitter_analyze" in st.session_state and st.session_state.twitter_analyze:
        handle_twitter_analysis(sentiment_engine)
        st.session_state.twitter_analyze = False
    elif "reddit_analyze" in st.session_state and st.session_state.reddit_analyze:
        handle_reddit_analysis(sentiment_engine)
        st.session_state.reddit_analyze = False

def handle_facebook_analysis(sentiment_engine):
    st.header("Facebook Sentiment Analysis")
    
    config = st.session_state.get('facebook_config', {})
    page_id = config.get('page_id')
    access_token = config.get('access_token')
    post_limit = config.get('post_limit', 20)

    if page_id and access_token:
        with st.spinner("Fetching Facebook posts..."):
            try:
                analyzer = FacebookAnalyzer(access_token)
                posts = analyzer.get_posts(page_id, post_limit)

                if posts:
                    sentiment_data = []
                    for post in posts:
                        sentiment = sentiment_engine.analyze_sentiment(post['message'])
                        sentiment_data.append({
                            'post_id': post['id'],
                            'message': post['message'][:100] + "...",
                            'created_time': post['created_time'],
                            'sentiment': sentiment['label'],
                            'confidence': sentiment['score'],
                            'positive': sentiment['positive'],
                            'negative': sentiment['negative'],
                            'neutral': sentiment['neutral']
                        })

                    display_results(sentiment_data, "Facebook")
                else:
                    st.error("No posts found or unable to fetch posts.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.error("Configuration missing. Please configure Facebook settings first.")

def handle_instagram_analysis(sentiment_engine):
    st.header("Instagram Sentiment Analysis")
    
    config = st.session_state.get('instagram_config', {})
    username = config.get('username')
    post_limit = config.get('post_limit', 20)
    use_demo_data = config.get('use_demo_data', False)

    if username or use_demo_data:
        with st.spinner("Fetching Instagram posts..."):
            try:
                if use_demo_data:
                    alternative_analyzer = InstagramAlternativeAnalyzer()
                    posts = alternative_analyzer.create_sentiment_demo_posts(post_limit)
                    st.info("Using demo data with varied sentiment for analysis demonstration.")
                else:
                    analyzer = InstagramAnalyzer()
                    posts = analyzer.get_posts(username, post_limit)

                if posts:
                    sentiment_data = []
                    for post in posts:
                        sentiment = sentiment_engine.analyze_sentiment(post['caption'])
                        sentiment_data.append({
                            'post_id': post['shortcode'],
                            'message': post['caption'][:100] + "...",
                            'created_time': post['date'],
                            'sentiment': sentiment['label'],
                            'confidence': sentiment['score'],
                            'positive': sentiment['positive'],
                            'negative': sentiment['negative'],
                            'neutral': sentiment['neutral'],
                            'likes': post['likes'],
                            'comments': post['comments']
                        })

                    display_results(sentiment_data, "Instagram")
                else:
                    st.error("No posts found or unable to fetch posts.")

            except Exception as e:
                error_msg = str(e)
                if "rate limit" in error_msg.lower() or "401" in error_msg or "429" in error_msg:
                    st.error("Instagram Rate Limit Detected!")
                    st.warning("Instagram has temporarily blocked requests. Please try one of these options:")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Try Demo Data"):
                            try:
                                alternative_analyzer = InstagramAlternativeAnalyzer()
                                demo_posts = alternative_analyzer.create_sentiment_demo_posts(post_limit)

                                sentiment_data = []
                                for post in demo_posts:
                                    sentiment = sentiment_engine.analyze_sentiment(post['caption'])
                                    sentiment_data.append({
                                        'post_id': post['shortcode'],
                                        'message': post['caption'][:100] + "...",
                                        'created_time': post['date'],
                                        'sentiment': sentiment['label'],
                                        'confidence': sentiment['score'],
                                        'positive': sentiment['positive'],
                                        'negative': sentiment['negative'],
                                        'neutral': sentiment['neutral'],
                                        'likes': post['likes'],
                                        'comments': post['comments']
                                    })

                                st.success("Demo data loaded successfully!")
                                display_results(sentiment_data, "Instagram (Demo)")

                            except Exception as demo_error:
                                st.error(f"Error loading demo data: {demo_error}")

                    with col2:
                        st.info("**Wait and Retry**\n\nWait 10-15 minutes and try again with a different username or smaller post limit.")

                    st.markdown("---")
                    st.markdown("**Rate Limiting Tips:**")
                    st.markdown("• Instagram actively prevents automated access")
                    st.markdown("• Try smaller post limits (10-15 posts)")
                    st.markdown("• Wait between requests")
                    st.markdown("• Consider using the demo data for testing")

                else:
                    st.error(f"Error: {error_msg}")

                    if st.button("Load Demo Data Instead"):
                        try:
                            alternative_analyzer = InstagramAlternativeAnalyzer()
                            demo_posts = alternative_analyzer.create_sentiment_demo_posts(min(post_limit, 15))

                            sentiment_data = []
                            for post in demo_posts:
                                sentiment = sentiment_engine.analyze_sentiment(post['caption'])
                                sentiment_data.append({
                                    'post_id': post['shortcode'],
                                    'message': post['caption'][:100] + "...",
                                    'created_time': post['date'],
                                    'sentiment': sentiment['label'],
                                    'confidence': sentiment['score'],
                                    'positive': sentiment['positive'],
                                    'negative': sentiment['negative'],
                                    'neutral': sentiment['neutral'],
                                    'likes': post['likes'],
                                    'comments': post['comments']
                                })

                            st.success("Demo data loaded for analysis!")
                            display_results(sentiment_data, "Instagram (Demo)")

                        except Exception as demo_error:
                            st.error(f"Error loading demo data: {demo_error}")
    else:
        st.error("Configuration missing. Please configure Instagram settings first.")

def handle_twitter_analysis(sentiment_engine):
    st.header("Twitter/X Sentiment Analysis")
    
    config = st.session_state.get('twitter_config', {})
    bearer_token = config.get('bearer_token')
    search_query = config.get('search_query')
    tweet_limit = config.get('tweet_limit', 30)

    if bearer_token and search_query:
        with st.spinner("Fetching tweets..."):
            try:
                analyzer = TwitterAnalyzer(bearer_token)
                tweets = analyzer.get_tweets(search_query, tweet_limit)

                if tweets:
                    sentiment_data = []
                    for tweet in tweets:
                        sentiment = sentiment_engine.analyze_sentiment(tweet['text'])
                        sentiment_data.append({
                            'post_id': tweet['id'],
                            'message': tweet['text'][:100] + "...",
                            'created_time': tweet['created_at'],
                            'sentiment': sentiment['label'],
                            'confidence': sentiment['score'],
                            'positive': sentiment['positive'],
                            'negative': sentiment['negative'],
                            'neutral': sentiment['neutral'],
                            'retweets': tweet.get('public_metrics', {}).get('retweet_count', 0),
                            'likes': tweet.get('public_metrics', {}).get('like_count', 0)
                        })

                    display_results(sentiment_data, "Twitter")
                else:
                    st.error("No tweets found or unable to fetch tweets.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.error("Configuration missing. Please configure Twitter settings first.")

def handle_reddit_analysis(sentiment_engine):
    st.header("Reddit Sentiment Analysis")
    
    config = st.session_state.get('reddit_config', {})
    client_id = config.get('client_id')
    client_secret = config.get('client_secret')
    user_agent = config.get('user_agent', 'SentimentAnalyzer:v1.0')
    subreddit = config.get('subreddit')
    post_limit = config.get('post_limit', 25)

    if client_id and client_secret and subreddit:
        with st.spinner("Fetching Reddit posts..."):
            try:
                analyzer = RedditAnalyzer(client_id, client_secret, user_agent)
                posts = analyzer.get_posts(subreddit, post_limit)

                if posts:
                    sentiment_data = []
                    for post in posts:
                        sentiment = sentiment_engine.analyze_sentiment(post['title'] + " " + post['selftext'])
                        sentiment_data.append({
                            'post_id': post['id'],
                            'message': (post['title'] + " " + post['selftext'])[:100] + "...",
                            'created_time': post['created_utc'],
                            'sentiment': sentiment['label'],
                            'confidence': sentiment['score'],
                            'positive': sentiment['positive'],
                            'negative': sentiment['negative'],
                            'neutral': sentiment['neutral'],
                            'score': post['score'],
                            'comments': post['num_comments']
                        })

                    display_results(sentiment_data, "Reddit")
                else:
                    st.error("No posts found or unable to fetch posts.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.error("Configuration missing. Please configure Reddit settings first.")

def display_results(sentiment_data, platform):
    df = pd.DataFrame(sentiment_data)

    col1, col2, col3, col4 = st.columns(4)

    total_posts = len(df)
    positive_count = len(df[df['sentiment'] == 'Positive'])
    negative_count = len(df[df['sentiment'] == 'Negative'])
    neutral_count = len(df[df['sentiment'] == 'Neutral'])

    with col1:
        st.metric("Total Posts", total_posts)
    with col2:
        st.metric("Positive", positive_count, f"{positive_count/total_posts*100:.1f}%")
    with col3:
        st.metric("Negative", negative_count, f"{negative_count/total_posts*100:.1f}%")
    with col4:
        st.metric("Neutral", neutral_count, f"{neutral_count/total_posts*100:.1f}%")

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trends", "Data", "Word Cloud"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            sentiment_counts = df['sentiment'].value_counts()
            fig_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title=f"{platform} Sentiment Distribution",
                color_discrete_map={
                    'Positive': '#2ecc71',
                    'Negative': '#e74c3c',
                    'Neutral': '#95a5a6'
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            fig_conf = px.histogram(
                df, x='confidence', color='sentiment',
                title="Confidence Score Distribution",
                color_discrete_map={
                    'Positive': '#2ecc71',
                    'Negative': '#e74c3c',
                    'Neutral': '#95a5a6'
                }
            )
            st.plotly_chart(fig_conf, use_container_width=True)

    with tab2:
        if 'created_time' in df.columns:
            df['created_time'] = pd.to_datetime(df['created_time'])
            df['date'] = df['created_time'].dt.date

            daily_sentiment = df.groupby(['date', 'sentiment']).size().reset_index(name='count')

            fig_timeline = px.line(
                daily_sentiment, x='date', y='count', color='sentiment',
                title=f"{platform} Sentiment Trends Over Time",
                color_discrete_map={
                    'Positive': '#2ecc71',
                    'Negative': '#e74c3c',
                    'Neutral': '#95a5a6'
                }
            )
            st.plotly_chart(fig_timeline, use_container_width=True)

        fig_scatter = px.scatter(
            df, x='positive', y='negative', color='sentiment',
            title="Sentiment Score Scatter Plot",
            hover_data=['confidence'],
            color_discrete_map={
                'Positive': '#2ecc71',
                'Negative': '#e74c3c',
                'Neutral': '#95a5a6'
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab3:
        st.subheader("Detailed Results")
        display_df = df[['message', 'sentiment', 'confidence', 'created_time']].copy()
        st.dataframe(display_df, use_container_width=True)

        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{platform}_sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    with tab4:
        st.subheader("Word Cloud")
        st.info("Word cloud visualization will be implemented here using the wordcloud library")

        all_text = " ".join(df['message'].str.replace("...", ""))
        words = all_text.split()
        word_freq = pd.Series(words).value_counts().head(20)

        fig_words = px.bar(
            x=word_freq.values, y=word_freq.index,
            orientation='h',
            title="Top 20 Most Frequent Words",
            labels={'x': 'Frequency', 'y': 'Words'}
        )
        fig_words.update_layout(height=600)
        st.plotly_chart(fig_words, use_container_width=True)

if __name__ == "__main__":
    main()
