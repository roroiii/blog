# 替換 tweepy.TweepError 的使用
try:
    from tweepy.errors import TweepyException  # 新版 Tweepy
except ImportError:
    try:
        from tweepy import TweepError as TweepyException  # 舊版 Tweepy 的兼容
    except ImportError:
        from tweepy import TweepError  # 更舊的版本

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
github_repo_url = "https://github.com/roroiii/blog.git"  # 替換為你的倉庫 URL
github_token = os.getenv("X_GITHUB_TOKEN")  # 從 GitHub Actions 提供的 GITHUB_TOKEN 獲取

# 關鍵字列表
keywords = ["書摘", "閱讀", "書籍"] 

# 已處理的推文 ID 記錄（避免重複發佈）
processed_tweets = set()
processed_tweets_file = os.path.join(repo_path, "processed_tweets.txt")

# 初始化 X API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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

# 獲取推文
def fetch_tweets():
    try:
        # 取得當前用戶的 screen_name
        current_user = api.verify_credentials()
        tweets = api.user_timeline(screen_name=current_user.screen_name, count=100, tweet_mode="extended")
        return tweets
    except Exception as e:  # 使用更通用的異常處理
        print(f"Error fetching tweets: {e}")
        return []

# 將推文轉換為 11ty 書摘 Markdown 格式
def tweet_to_markdown(tweet):
    tweet_text = tweet.full_text
    tweet_id = tweet.id
    date_str = datetime.now().strftime("%Y-%m-%d")
    # 生成安全的文件名
    filename = f"book-{date_str}.md"
    filepath = os.path.join(books_dir, filename)
    
    # 檢查是否已存在同日期檔案，若存在則追加序號
    counter = 1
    while os.path.exists(filepath):
        filename = f"book-{date_str}-{counter}.md"
        filepath = os.path.join(books_dir, filename)
        counter += 1
    
    # Front Matter 和內容
    content = f"""---
title: "書摘：來自 X 的分享"
tags: [hippocampus, book]
date: '{date_str}'
image: '/images/books/default-book-cover.webp'
---

{tweet_text}


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

# 處理推文並更新博客
def process_tweets():
    global processed_tweets
    processed_tweets = load_processed_tweets()
    tweets = fetch_tweets()
    repo = git.Repo(repo_path)
    
    for tweet in tweets:
        if tweet.id not in processed_tweets:
            tweet_text = tweet.full_text
            # 檢查是否包含關鍵字
            if any(keyword.lower() in tweet_text.lower() for keyword in keywords):
                print(f"Found matching tweet: {tweet_text}")
                filepath, content = tweet_to_markdown(tweet)
                # 寫入 Markdown 文件
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                # 提交到 GitHub
                commit_to_github(repo, filepath, tweet.id)
                processed_tweets.add(tweet.id)
    
    # 儲存已處理的推文 ID
    save_processed_tweets()

if __name__ == "__main__":
    print("Starting X to 11ty Book automation...")
    # 確保 books 目錄存在
    os.makedirs(books_dir, exist_ok=True)
    process_tweets()