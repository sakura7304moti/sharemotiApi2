import datetime
import os
import pandas as pd
import yaml
# プロジェクトの相対パス
_base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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