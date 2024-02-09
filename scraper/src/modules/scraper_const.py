import datetime
import os
import pandas as pd
import yaml
from typing import List
# プロジェクトの相対パス
_base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 空文字用の定数
def get_new_line_text() -> str:
    return "jsdlkjflasjfiojadispfosdjfposdj"

# hololive fanart tag list
def holoList():
    holo_path = os.path.join(_base_path, "options", "HoloFanArt.csv")
    df = pd.read_csv(holo_path)
    records = []
    for index, row in df.iterrows():
        hashtag = row["hashtag"]
        url = row["url"]
        rec = HoloName(hashtag,url)
        records.append(rec)
    return records

#ホロメン一覧
def holoMember():
    holo_path = os.path.join(_base_path, "options", "holoMember.csv")
    df = pd.read_csv(holo_path)
    word_list = df["member"].tolist()
    return word_list

def _url() -> dict:
    yaml_path = os.path.join(_base_path, "options", "url.yaml")
    with open(yaml_path) as file:
        yml = yaml.safe_load(file)
    return yml

#youtube チャンネル一覧
def channel_list():
    path = os.path.join(_base_path,'options','channel_list.csv')
    df = pd.read_csv(path)
    return df['0'].tolist()

def archive_dict_path():
    return os.path.join(_base_path,'options','archive_dict.json')

#twitterのbaseハッシュタグ一覧
def twitter_base_hashtags():
    path = os.path.join(_base_path,'options','twitter_base_hashtags.csv')
    df = pd.read_csv(path)
    return df['hashtag']

#URLまとめ
class UrlOption:
    def __init__(self):
        yml = _url()
        self.cover = yml['cover']
        self.ori = yml['ori']

# `Database` クラスには、Twitter データベース ファイルへのパスを返すメソッド `twitter_path` があります。
class Database:
    def twitter_path(self) -> str:
        return os.path.join(_base_path,'database','twitter.db')

    def youtube_path(self) -> str:
        return os.path.join(_base_path,'database','youtube.db')
    

# HoloName クラスは、ハッシュタグと URL のペアを表します。
class HoloName:
    def __init__(self,hashtag,url):
        self.hashtag = hashtag
        self.url = url

    def __dict__(self):
        return {"hashtag":self.hashtag,"url":self.url}
    
# `TwitterQueryRecord` クラスは、ハッシュタグ、モード、URL、日付、画像、ユーザー ID、ユーザー名、いいね数などの情報を含む Twitter クエリのレコードを表します。
class TwitterQueryRecord:
    hashtag: str
    mode: str
    url: str
    date: datetime.date
    images: list[str]
    userId: str
    userName: str
    likeCount: int

    def __init__(
        self,
        hashtag: str,
        mode: str,
        url: str,
        date: str,
        images: str,
        userId: str,
        userName: str,
        likeCount: int,
    ):
        self.hashtag = hashtag
        self.mode = mode
        self.url = url
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        self.images = images.split(",")
        self.userId = userId
        self.userName = userName
        self.likeCount = likeCount

    def __str__(self):
        return (
            f"Hashtag: {self.hashtag}\n"
            f"Mode: {self.mode}\n"
            f"URL: {self.url}\n"
            f"Date: {self.date}\n"
            f"Images: {self.images}\n"
            f"User ID: {self.userId}\n"
            f"User Name: {self.userName}\n"
            f"Like Count: {self.likeCount}\n"
        )

    def __dict__(self):
        return {
            "hashtag": self.hashtag,
            "mode": self.mode,
            "url": self.url,
            "date": self.date.strftime("%Y-%m-%d"),
            "images": self.images,
            "userId": self.userId,
            "userName": self.userName,
            "likeCount": self.likeCount,
        }
    
# `SongQueryRecord` クラスは、日付、メンバー、リンク、曲名、その他の詳細を含む曲クエリのレコードを表します。
class SongQueryRecord:
    date:str
    member:str
    link:str
    song_name:str
    detail:str

    def __init__(
            self,
            date:str,
            member:str,
            link:str,
            song_name:str,
            detail:str,
    ):
        self.date =date
        self.member = member
        self.link = link
        self.song_name = song_name
        self.detail = detail

    def __str__(self):
        return {
            f"Date:{self.date}\n"
            f"Member:{self.member}\n"
            f"Link:{self.link}\n"
            f"SongName:{self.song_name}\n"
            f"Detail:{self.detail}\n"
        }
    
    def __dict__(self):
        return {
            "date":self.date,
            "member":self.member,
            "link":self.link,
            "songName":self.song_name,
            "detail":self.detail
        }
    
# `HoloSongAlbum` クラスは、アルバム名、アーティスト、プレイリスト リンク、日付、画像リンクなどのプロパティを持つ曲アルバムを表します。
class HoloSongAlbum:
    albumName:str
    artist:str
    playlistLink:str
    date:str
    imageLink:str
    
    def __init__(self,albumName:str,artist:str,playlistLink:str,date:str,imageLink:str):
        self.albumName = albumName
        self.artist = artist
        self.playlistLink = playlistLink
        self.date = date
        self.imageLink = imageLink
        
    def __dict__(self):
        return {
            "albumName":self.albumName,
            "artist":self.artist,
            "playlistLink":self.playlistLink,
            "date":self.date,
            "imageLink":self.imageLink
        }
    
    def __str__(self):
        return f"Album Name: {self.albumName}\nArtist: {self.artist}\nPlaylist Link: {self.playlistLink}\nDate: {self.date}\nImage Link: {self.imageLink}"
    
class HoloMemoryRecord:
    title: str
    member: str
    date: str
    link:str
    memory: str
    detail: str

    def __init__(self, title: str, member: str, date: str, link:str, memory: str, detail: str):
        self.title = title
        self.member = member
        self.link = link
        self.date = date
        self.memory = memory
        self.detail = detail

    def __dict__(self):
        return {
            "title": self.title,
            "member": self.member,
            "link":self.link,
            "date": self.date,
            "memory": self.memory,
            "detail": self.detail
        }

    def __str__(self):
        return f"{self.title} - {self.member} - {self.link} - {self.date} - {self.memory} - {self.detail}"

class ChannelInfo:
    def __init__(self,channel_id,channel_name,description,header_url,avatar_url):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.description = description
        self.header_url = header_url
        self.avatar_url = avatar_url
        
    def __str__(self):
        return f"""channel_name -> {self.channel_name}
channel_id -> {self.channel_id}
header_url -> {self.header_url}
avatar_url -> {self.avatar_url}
---- description -----
{self.description}
        """
    
    def __dict__(self):
        return {
            "channelId":self.channel_id,
            "channelName":self.channel_name,
            "description":self.description,
            "headerUrl":self.header_url,
            "avatarUrl":self.avatar_url
        }


class MovieInfo:
    def __init__(self,id,url,title,date,channel_id,view_count,thumbnail_url,movie_type):
        self.id = id
        self.url = url
        self.title = title
        self.date = date
        self.channel_id = channel_id
        self.view_count = view_count
        self.thumbnail_url = thumbnail_url
        self.movie_type = movie_type

    def __str__(self):
        return f"""if -> {self.id}
url -> {self.url}
title -> {self.title}
date -> {self.date}
channel_id -> {self.channel_id}
view_count -> {self.view_count}
thumbnail_url -> {self.thumbnail_url}
movieType -> {self.movie_type}"""
    
    def __dict__(self):
        return {
            "id":self.id,
            "url":self.url,
            "title":self.title,
            "date":self.date,
            "channelId":self.channel_id,
            "viewCount":self.view_count,
            "thumbnailUrl":self.thumbnail_url,
            "movieType":self.movie_type
        }
    
    
class Archive:
    def __init__(self,channel:ChannelInfo,movie:List[MovieInfo],live:List[MovieInfo],short:List[MovieInfo]):
        self.channel = channel
        self.movie = movie
        self.live = live
        self.short = short

    def __dict__(self):
        return {
            "channel": self.channel.__dict__(),
            "movie": [m.__dict__() for m in self.movie],
            "live": [l.__dict__() for l in self.live],
            "short": [s.__dict__() for s in self.short]
        }