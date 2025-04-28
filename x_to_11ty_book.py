import tweepy
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

# 路徑設定
repo_path = "."  # GitHub Actions 運行時在倉庫根目錄
books_dir = os.path.join(repo_path, "src", "books")  # 書摘目錄

# 關鍵字列表
keywords = ["書摘", "影集"]

# 已處理的推文 ID 記錄（避免重複發佈）
processed_tweets = set()
processed_tweets_file = os.path.join(repo_path, "processed_tweets.txt")

# 載入已處理的推文 ID
def load_processed_tweets():
    processed = set()
    if os.path.exists(processed_tweets_file):
        with open(processed_tweets_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and line.isdigit():  # 確保行不為空且是數字
                    processed.add(int(line))  # 轉換為整數
                else:
                    print(f"Skipping invalid line in {processed_tweets_file}: '{line}'")
            print(f"Loaded {len(processed)} processed tweet IDs from {processed_tweets_file}: {processed}")
    else:
        print(f"No processed tweets file found at {processed_tweets_file}")
    return processed

# 儲存已處理的推文 ID
def save_processed_tweets():
    print(f"Saving {len(processed_tweets)} processed tweet IDs to {processed_tweets_file}: {processed_tweets}")
    try:
        with open(processed_tweets_file, "w") as f:
            for tweet_id in sorted(processed_tweets):  # 排序以保持一致性
                f.write(f"{tweet_id}\n")
        print(f"Successfully saved processed tweet IDs to {processed_tweets_file}")
    except Exception as e:
        print(f"Error saving processed tweets to {processed_tweets_file}: {e}")

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
        print(f"Authenticated as user: {user.username}")
        tweets = client.get_users_tweets(
            id=user.id, 
            max_results=5, 
            tweet_fields=["created_at", "text"],
            user_auth=True
        )
        if not tweets.data:
            print("No tweets found.")
            return []
        print(f"Found {len(tweets.data)} tweets:")
        for tweet in tweets.data:
            print(f"Tweet ID: {tweet.id}, Text: {tweet.text}")
        return tweets.data
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []

# 將推文轉換為 11ty 書摘 Markdown 格式
def tweet_to_markdown(tweet):
  tweet_text = tweet.text
  tweet_id = tweet.id
  date_str = tweet.created_at.strftime("%Y-%m-%d")
  
  # 預先處理標題和內容
  lines = tweet_text.split('\n')
  first_line = lines[0].strip()
  remaining_text = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
  
  # 根據第一行內容決定檔名前綴
  if "影集" in first_line:
    filename_prefix = "video"
    tags = ["hippocampus", "video"]
  else:
    filename_prefix = "book"
    tags = ["hippocampus", "book"]
  
  filename = f"{filename_prefix}-{date_str}.md"
  filepath = os.path.join(books_dir, filename)
  
  counter = 1
  while os.path.exists(filepath):
    filename = f"{filename_prefix}-{date_str}-{counter}.md"
    filepath = os.path.join(books_dir, filename)
    counter += 1
  
  image_match = re.search(r'http\S+', tweet_text)
  image_url = image_match.group(0) if image_match else '/images/books/default-book-cover.webp'
  
  content = f"""---
title: '{first_line}'
tags: {tags}
date: '{date_str}'
image: '{image_url}'
---

{remaining_text}

"""
  print(f"Generated Markdown file: {filepath}")
  return filepath, content

# 處理推文並生成 Markdown 文件
def process_tweets():
    global processed_tweets
    processed_tweets = load_processed_tweets()
    tweets = fetch_tweets()
    
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    user = client.get_me().data
    screen_name = user.username
    
    if not tweets:
        print("No tweets to process.")
        return
    
    found_matching_tweet = False
    for tweet in tweets:
        if tweet.id not in processed_tweets:
            tweet_text = tweet.text
            if any(keyword.lower() in tweet_text.lower() for keyword in keywords):
                found_matching_tweet = True
                print(f"Found matching tweet: {tweet_text}")
                filepath, content = tweet_to_markdown(tweet)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Successfully created file for tweet {tweet.id}: {filepath}")
                processed_tweets.add(tweet.id)
            else:
                print(f"Tweet does not match keywords: {tweet_text}")
        else:
            print(f"Tweet already processed: {tweet.id}")
    
    if not found_matching_tweet:
        print("No new tweets matched the keywords.")
    
    save_processed_tweets()

if __name__ == "__main__":
    print("Starting X to 11ty Book automation...")
    os.makedirs(books_dir, exist_ok=True)
    process_tweets()