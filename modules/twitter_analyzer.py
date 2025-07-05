import tweepy
from datetime import datetime
import time

class TwitterAnalyzer:  
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.client = tweepy.Client(bearer_token=bearer_token)
    
    def get_tweets(self, query, limit=30, tweet_fields=None):
        try:
            if tweet_fields is None:
                tweet_fields = ['created_at', 'author_id', 'public_metrics', 'context_annotations', 'lang']
            
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=query,
                tweet_fields=tweet_fields,
                max_results=min(100, limit)
            ).flatten(limit=limit)
            
            tweet_list = []
            for tweet in tweets:
                tweet_data = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'author_id': tweet.author_id,
                    'public_metrics': tweet.public_metrics,
                    'lang': getattr(tweet, 'lang', 'unknown'),
                    'context_annotations': getattr(tweet, 'context_annotations', [])
                }
                tweet_list.append(tweet_data)
            
            return tweet_list
            
        except tweepy.TooManyRequests:
            raise Exception("Twitter API rate limit exceeded. Please wait before making more requests.")
        except tweepy.Unauthorized:
            raise Exception("Twitter API authentication failed. Check your Bearer Token.")
        except Exception as e:
            raise Exception(f"Error fetching tweets: {str(e)}")
    
    def get_user_tweets(self, username, limit=30):
        try:
            user = self.client.get_user(username=username)
            if not user.data:
                raise Exception(f"User '{username}' not found")
            
            user_id = user.data.id
            
            tweets = tweepy.Paginator(
                self.client.get_users_tweets,
                id=user_id,
                tweet_fields=['created_at', 'public_metrics', 'lang'],
                max_results=min(100, limit)
            ).flatten(limit=limit)
            
            tweet_list = []
            for tweet in tweets:
                tweet_data = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'author_id': user_id,
                    'author_username': username,
                    'public_metrics': tweet.public_metrics,
                    'lang': getattr(tweet, 'lang', 'unknown')
                }
                tweet_list.append(tweet_data)
            
            return tweet_list
            
        except Exception as e:
            raise Exception(f"Error fetching user tweets: {str(e)}")
    
    def get_tweet_replies(self, tweet_id, limit=10):
        try:
            query = f"conversation_id:{tweet_id}"
            
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=query,
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'in_reply_to_user_id'],
                max_results=min(100, limit)
            ).flatten(limit=limit)
            
            reply_list = []
            for tweet in tweets:
                if tweet.id != tweet_id:
                    reply_data = {
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'author_id': tweet.author_id,
                        'public_metrics': tweet.public_metrics,
                        'in_reply_to_user_id': getattr(tweet, 'in_reply_to_user_id', None)
                    }
                    reply_list.append(reply_data)
            
            return reply_list
            
        except Exception as e:
            raise Exception(f"Error fetching tweet replies: {str(e)}")
    
    def get_trending_topics(self, woeid=1):
        return ["Trending topics require API v1.1 access"]
    
    def get_user_info(self, username):
        try:
            user = self.client.get_user(
                username=username,
                user_fields=['created_at', 'description', 'public_metrics', 'verified']
            )
            
            if not user.data:
                raise Exception(f"User '{username}' not found")
            
            user_data = user.data
            return {
                'id': user_data.id,
                'username': user_data.username,
                'name': user_data.name,
                'description': getattr(user_data, 'description', ''),
                'created_at': getattr(user_data, 'created_at', None),
                'verified': getattr(user_data, 'verified', False),
                'public_metrics': getattr(user_data, 'public_metrics', {})
            }
            
        except Exception as e:
            raise Exception(f"Error fetching user info: {str(e)}")
    
    def validate_credentials(self):
        try:
            me = self.client.get_me()
            return me.data is not None
        except:
            return False
    
    @staticmethod
    def get_setup_instructions():
        return """
        Twitter/X API Setup Instructions:
        
        1. Go to https://developer.twitter.com/
        2. Apply for a developer account
        3. Create a new app in the developer portal
        4. Generate API keys and tokens:
           - API Key
           - API Secret Key
           - Bearer Token (required for this app)
           - Access Token & Secret (optional)
        5. Set up your app permissions
        6. Copy the Bearer Token for use in this application
        
        API Access Levels:
        - Essential (Free): 500,000 tweets/month
        - Elevated ($100/month): 2M tweets/month
        - Academic Research: Free for qualifying researchers
        
        Note: Twitter has implemented stricter API access policies.
        Make sure you comply with their terms of service.
        """
    
    @staticmethod
    def get_query_examples():
        return """
        Twitter Search Query Examples:
        
        1. Hashtags: #python OR #machinelearning
        2. Mentions: @elonmusk OR @twitter
        3. Keywords: "artificial intelligence" -retweets
        4. From user: from:nasa
        5. To user: to:support
        6. Language: lang:en
        7. Date range: since:2023-01-01 until:2023-12-31
        8. Media: has:media
        9. Links: has:links
        10. Verified users: is:verified
        
        Combine multiple criteria:
        "#AI lang:en -is:retweet has:media"
        """
