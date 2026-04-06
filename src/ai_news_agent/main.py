import os
import feedparser
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

if not EMAIL or not APP_PASSWORD:
    raise ValueError("EMAIL and APP_PASSWORD environment variables must be set")

RSS_FEEDS = [
    "https://arxiv.org/rss/cs.AI",
    "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
]

KEYWORDS = ["llm", "gpt", "openai", "agent", "rag", "ai", "machine learning"]


def fetch_articles():
    articles = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:10]:
            title = str(entry.title) if entry.title else ""
            link = entry.link

            if any(k in title.lower() for k in KEYWORDS):
                articles.append({"title": title, "link": link})

    return articles[:10]


def format_email(articles):
    today = datetime.now().strftime("%d %B %Y")
    content = f"🧠 AI Daily Digest - {today}\n\n"

    if not articles:
        return content + "No relevant news today."

    for i, a in enumerate(articles, 1):
        content += f"{i}. {a['title']}\n{a['link']}\n\n"

    return content


def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = "🧠 Daily AI News"
    msg["From"] = EMAIL or ""
    msg["To"] = EMAIL or ""

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL or "", APP_PASSWORD or "")
        server.send_message(msg)


def main():
    articles = fetch_articles()
    email_body = format_email(articles)
    send_email(email_body)


if __name__ == "__main__":
    main()
