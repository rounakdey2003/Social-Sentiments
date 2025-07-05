import requests
import json
import time
import random
from datetime import datetime

class InstagramAlternativeAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_sample_posts(self, username, limit=10):
        sample_posts = [
            {
                'shortcode': f'sample_post_{i}',
                'caption': f'Sample Instagram post #{i} from @{username}. This is a demonstration post with sample sentiment content. #instagram #sample #post',
                'date': datetime.now(),
                'likes': random.randint(10, 1000),
                'comments': random.randint(1, 50),
                'is_video': random.choice([True, False]),
                'url': f'https://www.instagram.com/p/sample_post_{i}/',
                'hashtags': ['instagram', 'sample', 'post'],
                'mentions': [username]
            }
            for i in range(1, min(limit + 1, 11))
        ]
        
        return sample_posts
    
    def get_posts_with_fallback(self, username, limit=20):
        try:            
            profile_url = f"https://www.instagram.com/{username}/"
            response = self.session.get(profile_url, timeout=10)
            
            if response.status_code == 200:
                posts = self.get_sample_posts(username, min(limit, 10))
                return {
                    'posts': posts,
                    'status': 'sample_data',
                    'message': f'Generated sample data for @{username}. For real data, Instagram API access is required.',
                    'real_data': False
                }
            else:
                raise Exception(f"Profile not accessible: HTTP {response.status_code}")
                
        except Exception as e:            
            posts = self.get_sample_posts('sample_user', min(limit, 5))
            return {
                'posts': posts,
                'status': 'fallback_data',
                'message': f'Unable to access @{username}. Showing sample data for demonstration. Error: {str(e)}',
                'real_data': False
            }
    
    def create_sentiment_demo_posts(self, count=15):
        positive_captions = [
            "Amazing day! Love this new product! 😍 #happy #love #awesome",
            "Best experience ever! Highly recommend! ⭐⭐⭐⭐⭐ #great #recommend",
            "Fantastic quality! Super satisfied with my purchase! #quality #satisfied",
            "Incredible service! Will definitely come back! #service #excellent",
            "Perfect! Everything exceeded my expectations! #perfect #exceeded"
        ]
        
        negative_captions = [
            "Terrible experience. Very disappointed. 😞 #disappointed #bad",
            "Poor quality for the price. Not worth it. #poor #expensive",
            "Worst customer service ever! Avoid this! #worst #avoid",
            "Complete waste of money. Don't buy this. #waste #money",
            "Horrible product. Broke after one day. #horrible #broken"
        ]
        
        neutral_captions = [
            "Regular product. Nothing special but okay. #okay #regular",
            "Standard quality. What you'd expect. #standard #expected",
            "It's fine. Does what it's supposed to do. #fine #functional",
            "Average experience. Could be better. #average #could_be_better",
            "Normal product. No complaints, no praise. #normal #standard"
        ]
        
        all_captions = positive_captions + negative_captions + neutral_captions
        posts = []
        
        for i in range(count):
            caption = random.choice(all_captions)
            posts.append({
                'shortcode': f'demo_post_{i}',
                'caption': caption,
                'date': datetime.now(),
                'likes': random.randint(5, 500),
                'comments': random.randint(0, 25),
                'is_video': random.choice([True, False]),
                'url': f'https://www.instagram.com/p/demo_post_{i}/',
                'hashtags': ['demo', 'sentiment', 'analysis'],
                'mentions': ['demo_user']
            })
        
        return posts
    
    @staticmethod
    def get_usage_instructions():        
        return """
        Instagram Alternative Analyzer Usage:
        
        This analyzer is designed as a fallback when the main Instagram 
        analyzer encounters rate limits or API restrictions.
        
        Features:
        1. Sample Data Generation: Creates realistic sample posts for testing
        2. Sentiment Demo Posts: Generates posts with varied sentiment
        3. Fallback Mechanism: Provides data when real API access fails
        
        Limitations:
        - Does not fetch real Instagram data
        - Generates sample/demo data for analysis purposes
        - Useful for testing and demonstration
        
        For real Instagram data, you need:
        - Official Instagram API access
        - Business/Creator account
        - Approved application
        
        This alternative is perfect for:
        - Testing sentiment analysis algorithms
        - Demonstrating the application
        - Development and prototyping
        """
