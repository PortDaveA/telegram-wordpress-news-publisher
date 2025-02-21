import os
import sys
import requests
import feedparser
import openai
import logging
import random  
from apscheduler.schedulers.blocking import BlockingScheduler
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# WordPress REST API endpoint and credentials
wordpress_url = "https://technews.redsaxon.com/wp-json/wp/v2/posts"
username = os.getenv("WORDPRESS_USERNAME")
application_password = os.getenv("WORDPRESS_APPLICATION_PASSWORD")

# Telegram Bot API Credentials
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Retry logic for requests
session = requests.Session()
retry = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# WordPress category mapping
wordpress_categories = {
    "History": 18,
    "Astronomy": 17,
    "Consumer Products": 15,
    "Consumer Electronics": 14,
    "Medicine": 13,
    "Paleontology": 12,
    "Sociology": 11,
    "Anthropology": 10,
    "Awards": 9,
    "Events": 8,
    "Environment": 7,
    "Mathematics": 6,
    "Physics": 5,
    "Chemistry": 4,
    "Biology": 3,
    "Technology": 2,
    "Uncategorised": 1
}

# Track published articles
published_links = set()

# List of RSS feeds
rss_feeds = [
    "https://www.sciencedaily.com/rss/top/science.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://phys.org/rss-feed/breaking/"
 
]

# Fetch articles from multiple RSS feeds
def fetch_articles():
    articles = []
    for feed_url in rss_feeds:
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                articles.extend([
                    {
                        "title": entry.get("title", "No title"),
                        "link": entry.get("link", ""),
                        "content": entry.get("summary", entry.get("description", "No content available"))
                    }
                    for entry in feed.entries
                ])
        except Exception as e:
            logging.error(f"Error fetching articles from {feed_url}: {e}")
    return articles

# Send message to Telegram
def send_to_telegram(title, content, link):
    if not telegram_bot_token or not telegram_chat_id:
        logging.error("Telegram bot token or chat ID not set.")
        return
    
    message = f"\U0001F4E2 *{title}*\n\n{content}\n\n\U0001F517 [Read more]({link})"
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(telegram_url, json=payload)
        if response.status_code == 200:
            logging.info("Message successfully sent to Telegram channel.")
        else:
            logging.error(f"Failed to send message. Response: {response.text}")
    except Exception as e:
        logging.error(f"Error sending message to Telegram: {e}")

# Publish content to WordPress
def publish_to_wordpress(title, content, category_name, link):
    try:
        if link in published_links:
            logging.info(f"Article already published: {link}")
            return

        category_id = wordpress_categories.get(category_name, wordpress_categories["Uncategorised"])
        data = {
            "title": title,
            "content": content,
            "status": "publish",
            "categories": [category_id]
        }

        headers = {'Content-Type': 'application/json'}
        response = session.post(
            wordpress_url,
            json=data,
            auth=(username, application_password),
            headers=headers
        )

        if response.status_code == 201:
            published_links.add(link)
            logging.info(f"Post published successfully: {response.json().get('link')}")
            send_to_telegram(title, content, link)
        else:
            logging.error(f"Failed to publish post. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"Error during WordPress post: {e}")

# Automation pipeline
def automation_pipeline():
    articles = fetch_articles()
    # Filter out articles that have already been published
    new_articles = [a for a in articles if a["link"] not in published_links]
    
    # Select up to 4 random articles from the new articles list
    random_articles = random.sample(new_articles, min(4, len(new_articles)))
    
    # Publish only these 4 randomly selected articles
    for article in random_articles:
        logging.info(f"Publishing article: {article['title']}")
        summarized_content = article["content"]
        publish_to_wordpress(article["title"], summarized_content, "Technology", article["link"])

# Scheduler setup
scheduler = BlockingScheduler()
# This job runs every 10 minutes, but it will only publish 4 articles at a time.
scheduler.add_job(automation_pipeline, 'cron', minute='*/10')

if __name__ == "__main__":
    try:
        logging.info("Starting automation scheduler...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")
