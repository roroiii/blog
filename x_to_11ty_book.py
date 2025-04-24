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
keywords = ["書摘", "影集"]

# 已處理的推文 ID 記錄（避免重複發佈）
processed_tweets = set()
processed_tweets_file = os.path.join(repo_path, "processed_tweets.txt")

# 載入已處理的推文 ID
def load_processed_tweets():
    if os.path.exists(processed_tweets_file):
        with open(processed_tweets_file, "r") as f:
            processed = set(line.strip() for line in f)
            print(f"Loaded {len(processed)} processed tweet IDs from {processed_tweets_file}")
            return processed
    print(f"No processed tweets file found at {processed_tweets_file}")
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
    image_match = re.search(r'http\S+', tweet_text)
    image_url = image_match.group(0) if image_match else '/images/books/default-book-cover.webp'
    tags = ["hippocampus", "book"] if "書摘" in first_line else ["hippocampus", "video"]
    
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

# 提交到 GitHub
def commit_to_github(repo, filepath, tweet_id):
    try:
        # 配置 Git 使用者資訊
        repo.git.config('user.email', 'github-actions[bot]@users.noreply.github.com')
        repo.git.config('user.name', 'GitHub Actions')
        
        # 設定遠端 URL
        origin = repo.remote(name="origin")
        origin.set_url(f"https://x-access-token:{github_token}@github.com/roroiii/blog.git")
        print(f"Set remote URL with token.")

        # 獲取當前分支名稱
        current_branch = repo.active_branch.name
        print(f"Current branch: {current_branch}")
        
        # 更明確的拉取和合併
        print("Fetching remote changes...")
        origin.fetch()
        
        print("Resetting local branch to match remote...")
        repo.git.reset(f"origin/{current_branch}", hard=True)
        
        # 檢查是否有變更
        repo.index.add([filepath])
        if repo.is_dirty():
            print(f"Changes detected, committing: {filepath}")
            repo.index.commit(f"Add book excerpt from tweet {tweet_id}")
            
            print("Pushing changes...")
            origin.push()
            print(f"Successfully pushed tweet {tweet_id} to GitHub")
        else:
            print("No changes to commit.")
    except Exception as e:
        print(f"Error committing to GitHub: {e}")
        import traceback
        traceback.print_exc()

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
                commit_to_github(repo, filepath, tweet.id)
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