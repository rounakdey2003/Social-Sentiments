import instaloader
from datetime import datetime
import time
import random

class InstagramAnalyzer:
    
    def __init__(self):
        self.loader = instaloader.Instaloader()        
        self.loader.context.log = lambda *args, **kwargs: None        
        self.loader.context.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.loader.context._session.headers.update({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def get_posts(self, username, limit=20):
        try:            
            time.sleep(random.uniform(2, 5))
                        
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            posts = []
            post_count = 0
            max_retries = 3
            retry_count = 0
            
            while post_count < limit and retry_count < max_retries:
                try:
                    for post in profile.get_posts():
                        if post_count >= limit:
                            break
                                                
                        try:
                            post_data = {
                                'shortcode': post.shortcode,
                                'caption': post.caption or "",
                                'date': post.date_utc,
                                'likes': getattr(post, 'likes', 0),
                                'comments': getattr(post, 'comments', 0),
                                'is_video': getattr(post, 'is_video', False),
                                'url': f"https://www.instagram.com/p/{post.shortcode}/",
                                'hashtags': list(post.caption_hashtags) if post.caption else [],
                                'mentions': list(post.caption_mentions) if post.caption else []
                            }
                            
                            posts.append(post_data)
                            post_count += 1
                                                        
                            time.sleep(random.uniform(1, 3))
                            
                        except Exception as post_error:
                            print(f"Warning: Skipping post due to error: {post_error}")
                            continue
                            
                    break
                    
                except Exception as e:
                    retry_count += 1
                    if "rate limit" in str(e).lower() or "429" in str(e) or "401" in str(e):
                        wait_time = random.uniform(60, 120) * retry_count
                        print(f"Rate limit detected. Waiting {wait_time:.0f} seconds before retry {retry_count}/{max_retries}")
                        time.sleep(wait_time)
                    else:
                        raise e
            
            if not posts and retry_count >= max_retries:
                raise Exception("Unable to fetch posts after multiple retries. Instagram may have rate limited the requests.")
            
            return posts
            
        except instaloader.exceptions.ProfileNotExistsException:
            raise Exception(f"Instagram profile '{username}' does not exist")
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            raise Exception(f"Instagram profile '{username}' is private")
        except Exception as e:
            if "rate limit" in str(e).lower() or "401" in str(e) or "429" in str(e):
                raise Exception(f"Instagram rate limit exceeded. Please wait 10-15 minutes before trying again. Original error: {str(e)}")
            else:
                raise Exception(f"Error fetching Instagram posts: {str(e)}")
    
    def get_profile_info(self, username):
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            return {
                'username': profile.username,
                'full_name': profile.full_name,
                'biography': profile.biography,
                'followers': profile.followers,
                'followees': profile.followees,
                'posts_count': profile.mediacount,
                'is_private': profile.is_private,
                'is_verified': profile.is_verified,
                'profile_pic_url': profile.profile_pic_url
            }
            
        except Exception as e:
            raise Exception(f"Error fetching profile info: {str(e)}")
    
    def get_post_comments(self, shortcode, limit=10):
        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            
            comments = []
            comment_count = 0
            
            for comment in post.get_comments():
                if comment_count >= limit:
                    break
                
                comment_data = {
                    'id': comment.id,
                    'text': comment.text,
                    'created_at': comment.created_at_utc,
                    'author': comment.owner.username,
                    'likes': comment.likes_count if hasattr(comment, 'likes_count') else 0
                }
                
                comments.append(comment_data)
                comment_count += 1
                                
                time.sleep(0.5)
            
            return comments
            
        except Exception as e:
            raise Exception(f"Error fetching comments: {str(e)}")
    
    def search_hashtag(self, hashtag, limit=20):
        try:
            hashtag_obj = instaloader.Hashtag.from_name(self.loader.context, hashtag)
            
            posts = []
            post_count = 0
            
            for post in hashtag_obj.get_posts():
                if post_count >= limit:
                    break
                
                post_data = {
                    'shortcode': post.shortcode,
                    'caption': post.caption or "",
                    'date': post.date_utc,
                    'likes': post.likes,
                    'comments': post.comments,
                    'owner': post.owner_username,
                    'url': f"https://www.instagram.com/p/{post.shortcode}/",
                    'hashtags': list(post.caption_hashtags) if post.caption else []
                }
                
                posts.append(post_data)
                post_count += 1
                
                time.sleep(2)
            
            return posts
            
        except Exception as e:
            raise Exception(f"Error searching hashtag: {str(e)}")
    
    def login(self, username, password):
        try:
            self.loader.login(username, password)
            return True
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")
    
    @staticmethod
    def get_setup_instructions():
        return """
        Instagram Analyzer Setup Instructions:
        
        1. No API key required for basic public profile access
        2. For better access and fewer limitations:
           - Create an Instagram account
           - Use the login feature (optional)
        3. Be aware of Instagram's rate limiting:
           - Don't make too many requests quickly
           - The tool includes automatic delays
        4. Private profiles cannot be accessed without following
        5. Some data may be limited for business/creator accounts
        
        Note: Instagram actively prevents automated access. Use responsibly
        and in accordance with Instagram's Terms of Service.
        
        For business use cases, consider Instagram's official APIs:
        - Instagram Basic Display API
        - Instagram Graph API (for business accounts)
        """
