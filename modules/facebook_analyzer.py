import requests
import json
from datetime import datetime
import time

class FacebookAnalyzer:
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def get_posts(self, page_id, limit=20):
        try:
            url = f"{self.base_url}/{page_id}/posts"
            params = {
                'access_token': self.access_token,
                'fields': 'id,message,created_time,likes.summary(true),comments.summary(true),shares',
                'limit': limit
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for post in data.get('data', []):
                if 'message' not in post:
                    continue
                
                post_data = {
                    'id': post['id'],
                    'message': post['message'],
                    'created_time': self._parse_facebook_time(post['created_time']),
                    'likes': post.get('likes', {}).get('summary', {}).get('total_count', 0),
                    'comments': post.get('comments', {}).get('summary', {}).get('total_count', 0),
                    'shares': post.get('shares', {}).get('count', 0)
                }
                posts.append(post_data)
            
            return posts
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Facebook API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing Facebook data: {str(e)}")
    
    def get_page_info(self, page_id):
        try:
            url = f"{self.base_url}/{page_id}"
            params = {
                'access_token': self.access_token,
                'fields': 'id,name,category,fan_count,talking_about_count'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Facebook API error: {str(e)}")
    
    def get_post_comments(self, post_id, limit=10):
        try:
            url = f"{self.base_url}/{post_id}/comments"
            params = {
                'access_token': self.access_token,
                'fields': 'id,message,created_time,from,like_count',
                'limit': limit
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            comments = []
            
            for comment in data.get('data', []):
                if 'message' in comment:
                    comment_data = {
                        'id': comment['id'],
                        'message': comment['message'],
                        'created_time': self._parse_facebook_time(comment['created_time']),
                        'author': comment.get('from', {}).get('name', 'Unknown'),
                        'likes': comment.get('like_count', 0)
                    }
                    comments.append(comment_data)
            
            return comments
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Facebook API error: {str(e)}")
    
    def _parse_facebook_time(self, time_string):
        try:
            return datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            try:
                return datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S+0000")
            except ValueError:
                return datetime.now()
    
    def validate_token(self):
        try:
            url = f"{self.base_url}/me"
            params = {'access_token': self.access_token}
            
            response = requests.get(url, params=params)
            return response.status_code == 200
            
        except:
            return False

    @staticmethod
    def get_setup_instructions():
        return """
        Facebook API Setup Instructions:
        
        1. Go to https://developers.facebook.com/
        2. Create a new app or use an existing one
        3. Add the Facebook Graph API product
        4. Generate an access token with the following permissions:
           - pages_read_engagement
           - pages_show_list (if accessing your own pages)
        5. For public pages, you may need to submit for app review
        6. Copy the access token and page ID for use in this application
        
        Note: Facebook has strict policies for data access. Make sure you comply
        with their terms of service and privacy policies.
        """
