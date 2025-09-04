# 🔗 Link: https://socialsentiment.streamlit.app
---
# Social Media Sentiment Analyzer

A comprehensive sentiment analysis tool for multiple social media platforms including Facebook, Instagram, Twitter/X, and Reddit. Built with Streamlit and powered by advanced NLP techniques.

## Features

- **Multi-Platform Support**: Analyze sentiment across Facebook, Instagram, Twitter/X, and Reddit
- **Advanced Sentiment Analysis**: Combines VADER and TextBlob for accurate sentiment scoring
- **Interactive Dashboard**: Beautiful Streamlit interface with real-time visualizations
- **Comprehensive Analytics**: 
  - Sentiment distribution charts
  - Time-based trend analysis
  - Word clouds
  - Detailed metrics and statistics
- **Rate Limit Handling**: Smart fallback mechanisms for API limitations
- **Demo Data Support**: Test the application with sample data when APIs are unavailable

## Quick Start

### Prerequisites

- Python 3.8 or higher
- API credentials for the platforms you want to analyze (see [API Setup](#api-setup))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SocialAnalyser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🔧 API Setup

### Facebook API

1. Visit [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or use existing one
3. Add Facebook Graph API product
4. Generate access token with permissions:
   - `pages_read_engagement`
   - `pages_show_list`
5. Copy the access token and page ID

### Twitter/X API

1. Apply for developer account at [Twitter Developer](https://developer.twitter.com/)
2. Create a new app
3. Generate Bearer Token
4. Copy the Bearer Token

**API Access Levels:**
- Essential (Free): 500,000 tweets/month
- Elevated ($100/month): 2M tweets/month
- Academic Research: Free for qualifying researchers

### Reddit API

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App"
3. Select "script" as app type
4. Note down:
   - Client ID (under app name)
   - Client Secret
5. Create user agent: `"platform:app_id:version by u/username"`

### Instagram

- **No API required** for basic public profile access
- Uses web scraping with rate limiting
- For better access, consider Instagram's official APIs:
  - Instagram Basic Display API
  - Instagram Graph API (for business accounts)

## 📁 Project Structure

```
SocialAnalyser/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                   # Environment variables template
├── README.md                      # Project documentation
└── modules/
    ├── facebook_analyzer.py       # Facebook data fetching
    ├── instagram_analyzer.py      # Instagram web scraping
    ├── instagram_alternative.py   # Instagram fallback analyzer
    ├── twitter_analyzer.py        # Twitter/X API integration
    ├── reddit_analyzer.py         # Reddit API integration
    └── sentiment_engine.py        # Sentiment analysis engine
```

## Usage Guide

### 1. Platform Selection
- Choose from Facebook, Instagram, Twitter/X, or Reddit
- Each platform has its own configuration dialog

### 2. Configuration
Click the analysis button for your chosen platform to configure:

**Facebook:**
- Page ID
- Access Token
- Number of posts to analyze (10-100)

**Instagram:**
- Username
- Number of posts (10-50)
- Demo data option for rate limits

**Twitter/X:**
- Bearer Token
- Search query (hashtags, keywords, @username)
- Number of tweets (10-100)

**Reddit:**
- Client ID and Secret
- User Agent
- Subreddit name
- Number of posts (10-100)

### 3. Analysis Results
View comprehensive analytics including:
- **Overview**: Sentiment distribution pie chart and metrics
- **Trends**: Time-based sentiment analysis
- **Data**: Raw data table with sentiment scores
- **Word Cloud**: Visual representation of frequently used words

## Sentiment Analysis Engine

The sentiment analysis combines two powerful approaches:

### VADER Sentiment
- Specialized for social media text
- Handles emojis, slang, and informal language
- Provides compound scores from -1 (negative) to +1 (positive)

### TextBlob
- General-purpose sentiment analysis
- Provides polarity and subjectivity scores
- Good for formal text analysis

### Combined Scoring
- **70% VADER weight** + **30% TextBlob weight**
- Threshold-based classification:
  - Positive: score ≥ 0.05
  - Negative: score ≤ -0.05
  - Neutral: -0.05 < score < 0.05

## Analytics Features

### Real-time Metrics
- Total posts analyzed
- Positive/Negative/Neutral counts and percentages
- Average sentiment scores

### Visualizations
- **Pie Charts**: Sentiment distribution
- **Bar Charts**: Sentiment comparison
- **Line Charts**: Temporal sentiment trends
- **Word Clouds**: Most frequent terms

### Data Export
- View raw data with sentiment scores
- Sortable and filterable tables
- Export capabilities for further analysis

## Rate Limits & Best Practices

### Instagram
- Strict rate limiting (~200 requests/hour)
- Automatic delays between requests
- Fallback to demo data when limited
- Wait 10-15 minutes between heavy usage

### Twitter/X
- 300 requests per 15 minutes (Essential)
- 1500 requests per 15 minutes (Elevated)
- Automatic rate limit handling

### Reddit
- 100 requests per minute (OAuth)
- 60 requests per minute (script apps)
- Built-in request spacing

### Facebook
- Varies by app and permissions
- Business verification may be required
- Respect platform terms of service

## Development

### Adding New Platforms
1. Create analyzer class in `modules/`
2. Implement required methods:
   - `get_posts()`
   - `validate_credentials()`
   - `get_setup_instructions()`
3. Add platform configuration in `app.py`
4. Update UI components

### Extending Sentiment Analysis
- Modify `SentimentEngine` class
- Add new analysis libraries
- Adjust scoring weights
- Implement custom models

## Troubleshooting

### Common Issues

**API Authentication Failed**
- Verify API credentials in `.env`
- Check token expiration
- Ensure proper permissions

**Rate Limit Exceeded**
- Wait for rate limit reset
- Use demo data for testing
- Reduce request frequency

**Instagram Access Issues**
- Profile may be private
- Use demo data option
- Wait between requests

**Empty Results**
- Check search parameters
- Verify content exists
- Try different time ranges

### Error Messages
- All errors include helpful context
- Check API status pages
- Verify network connectivity

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review API documentation
3. Create an issue on GitHub

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment) for social media sentiment analysis
- [TextBlob](https://textblob.readthedocs.io/) for natural language processing
- All the social media platform APIs for data access

---

**Made with ❤️ by [Rounak Dey](https://github.com/rounakdey2003)**
