import praw
import time
import requests
import datetime
import pandas as pd
import csv

from tqdm import tqdm

from . import hololewd_sqlite
from . import scraper_const

def get_rows():
    # Reddit APIの認証情報を設定
    reddit = praw.Reddit(client_id='4RVSChBoyaoylsur-e9sCA',
                         client_secret='k6LhqTyupGOqlB3h4jVHDoeL95YQKQ',
                         user_agent='hololewd/1.0 by Significant_West6050')
    
    # サブレディットとフレアの設定
    subreddit = reddit.subreddit('Hololewd')
    records = []
    # ポストの一覧を取得
    new_posts = subreddit.new(limit = 1000)
    top_posts = subreddit.top(limit = 1000)
    
    # ポストの情報を出力
    for posts in [new_posts,top_posts]:
        for post in tqdm(posts , total = 1000):
            # フレアが指定されたものかつ画像を含むポストのみ表示
            if post.url.endswith(('jpg', 'jpeg', 'png', 'gif' , 'mp4')):
                created_utc = datetime.datetime.utcfromtimestamp(post.created_utc)
                created_local = created_utc.strftime('%Y-%m-%d %H:%M:%S')
                print(f"\r tweets {len(records)} | {created_local}",end="")
        
                if post.url not in [r[2] for r in records]:
                    records.append(
                        (post.title,
                        post.link_flair_text,
                        post.url,
                        created_local,
                        post.score)
                    )
    df = pd.DataFrame (
        records,
        columns=['title', 'flair_text', 'url' , 'date' , 'score']
    )
    return df

def flair_texts_update():
    records,cn = hololewd_sqlite.search(page_size=999999)
    flair_texts = sorted(list(set([r.flair_text for r in records])))

    csv_path = scraper_const.hololwed_flair_path()
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["flair_text"])
        for t in flair_texts:
            if t != 'Yagoo':
                writer.writerow([t])

def update_db():
    df = get_rows()
    for index, row in tqdm(df.iterrows(),total = len(df),desc="db update..."):
        hololewd_sqlite.insert_hololewd(
            row['flair_text'],
            row['url'],
            row['date'].split(' ')[0],
            row['score']
        )
    flair_texts_update()
    
