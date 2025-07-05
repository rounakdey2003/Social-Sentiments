import praw
from datetime import datetime
import time

class RedditAnalyzer:    
    def __init__(self, client_id, client_secret, user_agent):
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )            
            self.reddit.user.me()
        except Exception as e:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
    
    def get_posts(self, subreddit_name, limit=25, sort_type='hot'):
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
                        
            if sort_type == 'hot':
                posts_iterator = subreddit.hot(limit=limit)
            elif sort_type == 'new':
                posts_iterator = subreddit.new(limit=limit)
            elif sort_type == 'top':
                posts_iterator = subreddit.top(limit=limit, time_filter='week')
            elif sort_type == 'rising':
                posts_iterator = subreddit.rising(limit=limit)
            else:
                posts_iterator = subreddit.hot(limit=limit)
            
            posts = []
            for post in posts_iterator:                
                if post.stickied or post.is_self is None:
                    continue
                
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'selftext': post.selftext,
                    'author': str(post.author) if post.author else '[deleted]',
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'url': post.url,
                    'permalink': f"https://reddit.com{post.permalink}",
                    'subreddit': post.subreddit.display_name,
                    'is_self': post.is_self,
                    'link_flair_text': post.link_flair_text,
                    'over_18': post.over_18
                }
                posts.append(post_data)
            
            return posts
            
        except Exception as e:
            raise Exception(f"Error fetching Reddit posts: {str(e)}")
    
    def get_post_comments(self, post_id, limit=20):
        try:
            submission = self.reddit.submission(id=post_id)
            submission.comments.replace_more(limit=0)
            
            comments = []
            comment_count = 0
            
            for comment in submission.comments.list():
                if comment_count >= limit:
                    break
                
                if hasattr(comment, 'body') and comment.body != '[deleted]':
                    comment_data = {
                        'id': comment.id,
                        'body': comment.body,
                        'author': str(comment.author) if comment.author else '[deleted]',
                        'created_utc': datetime.fromtimestamp(comment.created_utc),
                        'score': comment.score,
                        'parent_id': comment.parent_id,
                        'depth': comment.depth
                    }
                    comments.append(comment_data)
                    comment_count += 1
            
            return comments
            
        except Exception as e:
            raise Exception(f"Error fetching comments: {str(e)}")
    
    def search_posts(self, query, subreddit_name=None, limit=25, sort='relevance', time_filter='all'):
        try:
            if subreddit_name:
                subreddit = self.reddit.subreddit(subreddit_name)
                search_results = subreddit.search(
                    query, 
                    limit=limit, 
                    sort=sort, 
                    time_filter=time_filter
                )
            else:
                search_results = self.reddit.subreddit('all').search(
                    query, 
                    limit=limit, 
                    sort=sort, 
                    time_filter=time_filter
                )
            
            posts = []
            for post in search_results:
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'selftext': post.selftext,
                    'author': str(post.author) if post.author else '[deleted]',
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'url': post.url,
                    'permalink': f"https://reddit.com{post.permalink}",
                    'subreddit': post.subreddit.display_name,
                    'is_self': post.is_self
                }
                posts.append(post_data)
            
            return posts
            
        except Exception as e:
            raise Exception(f"Error searching Reddit: {str(e)}")
    
    def get_subreddit_info(self, subreddit_name):
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            return {
                'display_name': subreddit.display_name,
                'title': subreddit.title,
                'description': subreddit.description,
                'subscribers': subreddit.subscribers,
                'active_user_count': subreddit.active_user_count,
                'created_utc': datetime.fromtimestamp(subreddit.created_utc),
                'over18': subreddit.over18,
                'public_description': subreddit.public_description,
                'lang': subreddit.lang
            }
            
        except Exception as e:
            raise Exception(f"Error fetching subreddit info: {str(e)}")
    
    def get_user_posts(self, username, limit=25, sort='new'):
        try:
            user = self.reddit.redditor(username)
            
            if sort == 'new':
                posts_iterator = user.submissions.new(limit=limit)
            elif sort == 'hot':
                posts_iterator = user.submissions.hot(limit=limit)
            elif sort == 'top':
                posts_iterator = user.submissions.top(limit=limit)
            else:
                posts_iterator = user.submissions.new(limit=limit)
            
            posts = []
            for post in posts_iterator:
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'selftext': post.selftext,
                    'author': str(post.author) if post.author else '[deleted]',
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'subreddit': post.subreddit.display_name,
                    'permalink': f"https://reddit.com{post.permalink}"
                }
                posts.append(post_data)
            
            return posts
            
        except Exception as e:
            raise Exception(f"Error fetching user posts: {str(e)}")
    
    def validate_credentials(self):        
        try:            
            self.reddit.subreddit('test').display_name
            return True
        except:
            return False
    
    @staticmethod
    def get_setup_instructions():        
        return """
        Reddit API Setup Instructions:
        
        1. Go to https://www.reddit.com/prefs/apps
        2. Click "Create App" or "Create Another App"
        3. Fill out the form:
           - Name: Your application name
           - App type: Select "script"
           - Description: Brief description of your app
           - About URL: Leave blank or add your website
           - Redirect URI: http://localhost:8080 (for script apps)
        4. Click "Create app"
        5. Note down the credentials:
           - Client ID: Found under the app name
           - Client Secret: The "secret" field
        6. Create a user agent string (format: "platform:app_id:version by u/username")
        
        Example User Agent: "web:sentiment_analyzer:v1.0 by u/yourusername"
        
        Rate Limits:
        - 100 requests per minute for OAuth apps
        - 60 requests per minute for script apps
        
        Note: Reddit's API is free but has rate limits.
        Always respect the API terms of service.
        """
    
    @staticmethod
    def get_popular_subreddits():        
        return [
            'news', 'worldnews', 'politics', 'technology', 'science',
            'askreddit', 'iama', 'todayilearned', 'explainlikeimfive',
            'movies', 'music', 'books', 'gaming', 'sports',
            'funny', 'pics', 'memes', 'wholesomememes',
            'cryptocurrency', 'investing', 'stocks', 'economy',
            'programming', 'python', 'machinelearning', 'datascience'
        ]
