from scraper.src.modules import twitter_sqlite,twitter_scraper,scraper_const
from tqdm import tqdm

DATE_RANGE = 14

"""
BASE
"""
base_hashtags = scraper_const.twitter_base_hashtags()
for hashtag in tqdm(base_hashtags,desc='base'):
    df = twitter_scraper.get_tweet(hashtag,DATE_RANGE)
    twitter_sqlite.update(df,hashtag,'base')

"""
HOLO
"""
holo_hashtags = [item.hashtag for item in scraper_const.holoList()]
for hashtag in tqdm(holo_hashtags,desc='holo'):
    df = twitter_scraper.get_tweet(hashtag,DATE_RANGE)
    twitter_sqlite.update(df,hashtag,'holo')