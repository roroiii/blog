import tweepy
import git
import os
from datetime import datetime
import re

# X API 認證設定
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# 驗證環境變數是否設置
if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
    raise ValueError("Missing X API credentials. Ensure CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, and ACCESS_TOKEN_SECRET are set in environment variables.")

# GitHub 倉庫設定
repo_path = "."  # GitHub Actions 運行時在倉庫根目錄
books_dir = os.path.join(repo_path, "src", "books")  # 書摘目錄
github_repo_url = "https://github.com/roroiii/blog.git"
github_token = os.getenv("GITHUB_TOKEN")  # 使用 GITHUB_TOKEN

# 關鍵字列表
keywords = ["書摘", "閱讀", "書籍"]

# 已處理的推文 ID 記錄（避免重複發佈）
processed_tweets = set()
processed_tweets_file = os.path.join(repo_path, "processed_tweets.txt")

# 載入已處理的推文 ID
def load_processed_tweets():
    if os.path.exists(processed_tweets_file):
        with open(processed_tweets_file, "r") as f:
            return set(line.strip() for line in f)
    return set()

# 儲存已處理的推文 ID
def save_processed_tweets():
    with open(processed_tweets_file, "w") as f:
        for tweet_id in processed_tweets:
            f.write(f"{tweet_id}\n")

# 獲取推文（使用 X API v2）
def fetch_tweets():
    try:
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        user = client.get_me().data
        tweets = client.get_users_tweets(id=user.id, max_results=100, tweet_fields=["created_at", "text"])
        return tweets.data if tweets.data else []
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []

# 將推文轉換為 11ty 書摘 Markdown 格式
def tweet_to_markdown(tweet):
    tweet_text = tweet.text
    tweet_id = tweet.id
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"book-{date_str}.md"
    filepath = os.path.join(books_dir, filename)
    
    counter = 1
    while os.path.exists(filepath):
        filename = f"book-{date_str}-{counter}.md"
        filepath = os.path.join(books_dir, filename)
        counter += 1
    
    # 預先處理標題和內容
    lines = tweet_text.split('\n')
    first_line = lines[0].strip()
    remaining_text = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
    
    content = f"""---
title: '{first_line}'
tags: [hippocampus, book]
date: '{date_str}'
image: '/images/books/default-book-cover.webp'
---

'{remaining_text}'

"""
    return filepath, content

# 提交到 GitHub
def commit_to_github(repo, filepath, tweet_id):
    try:
        repo.index.add([filepath])
        repo.index.commit(f"Add book excerpt from tweet {tweet_id}")
        origin = repo.remote(name="origin")
        origin.set_url(f"https://x-access-token:{github_token}@github.com/roroiii/blog.git")
        origin.push()
        print(f"Successfully pushed tweet {tweet_id} to GitHub")
    except Exception as e:
        print(f"Error committing to GitHub: {e}")

# 處理推文並更新 blog
def process_tweets():
    global processed_tweets
    processed_tweets = load_processed_tweets()
    tweets = fetch_tweets()
    repo = git.Repo(repo_path)
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    user = client.get_me().data
    screen_name = user.username
    
    for tweet in tweets:
        if tweet.id not in processed_tweets:
            tweet_text = tweet.text
            if any(keyword.lower() in tweet_text.lower() for keyword in keywords):
                print(f"Found matching tweet: {tweet_text}")
                filepath, content = tweet_to_markdown(tweet)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                commit_to_github(repo, filepath, tweet.id)
                processed_tweets.add(tweet.id)
    
    save_processed_tweets()

if __name__ == "__main__":
    print("Starting X to 11ty Book automation...")
    os.makedirs(books_dir, exist_ok=True)
    process_tweets()