import sqlite3
from typing import List
import yt_dlp
from tqdm import tqdm
import datetime
from . import scraper_const

channel_url_list = scraper_const.channel_list()


"""
検索用の関数
"""
def get_yt_info(url:str):
    """
    yt-dlpでチャンネルの情報を取得。数秒かかる。
    """
    # オプションを設定
    ydl_opts = {
        'quiet': True,  # 出力を非表示
        'extract_flat': True,  # プレイリスト内の各動画を一つのリストに展開
        # その他のオプションは必要に応じて設定
    }
    
    # yt-dlpオブジェクトを生成
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    
    # プレイリストからURLリストを取得
    with ydl:
        result = ydl.extract_info(url, download=False)
    return result

def get_channel_info(result):
    """
    チャンネルの情報を元にconst.ChannelInfoを作成
    """
    #チャンネルid
    channel_id = result['uploader_id']

    #チャンネル名
    channel_name = result['channel'].replace('"','')
    
    #概要
    description = ''
    try:
        description = result['description'].replace('"','')
    except:
        pass
    
    
    #ヘッダー画像URL
    header_url = ''
    try:
        for rec in result['thumbnails']:
            if 'resolution' in rec:
                if rec['resolution'] == '1920x1080':
                    header_url = rec['url']
    except:
        pass
                
    #プロフィール画像URL
    avatar_url = result['thumbnails'][-2]['url']
    return scraper_const.ChannelInfo(channel_id,channel_name,description,header_url,avatar_url)

def get_thumbnail_url(id):
    return f'http://img.youtube.com/vi/{id}/maxresdefault.jpg'

def get_movie_info(entrie):
    id = entrie['id']
    url = entrie['url']
    title = entrie['title'].replace('"','')
    if 'view_count' in entrie:
        view_count = entrie['view_count']
        thumbnail_url = get_thumbnail_url(id)
        return [id,url,title,view_count,thumbnail_url]
    else:
        return None
    
def get_movie_list(entries):
    movie_list = []
    for rec in entries:
        info = get_movie_info(rec)
        if info is not None:
            movie_info = scraper_const.MovieInfo(info[0],info[1],info[2],'',info[3],info[4],'')
            movie_list.append(movie_info)
    return movie_list

def inferece_channenl(url:str) -> scraper_const.Archive:
    """
    チャンネルの情報やアーカイブを取得する
    """
    result = get_yt_info(url)
    channel = get_channel_info(result)
    #動画
    movie = get_movie_list(result['entries'][0]['entries'])

    #ショート
    short = get_movie_list(result['entries'][1]['entries'])

    #live
    try:
        live = get_movie_list(result['entries'][2]['entries'])
    except:
        live = get_movie_list(result['entries'][1]['entries'])
        short = []

    archive = scraper_const.Archive(channel,movie,short,live)
    return archive

def get_upload_date(url:str):
    # オプションを設定
    ydl_opts = {
        'quiet': True,  # 出力を非表示
        'date':True,
        'output':'%(upload_date)'
        # その他のオプションは必要に応じて設定
    }
    
    # yt-dlpオブジェクトを生成
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    
    # プレイリストからURLリストを取得
    with ydl:
        result = ydl.extract_info(url, download=False)
        stamp = result['release_timestamp']
        return str(datetime.datetime.fromtimestamp(stamp))

def holo_archives() -> List[scraper_const.Archive]:
    archives = []
    for url in tqdm(channel_url_list,desc="get archives"):
        archive = inferece_channenl(url)
        archives.append(archive)
    return archives

def update_archives():
    #日付以外全て取得する
    archives = holo_archives()

    #追加前にレコード取得
    movies = search_movie()
    channels = search_channel()

    # ----- チャンネル単位のループ -----
    for archive in tqdm(archives,desc="archives"):
        #チャンネルの追加・更新
        if archive.channel.channel_id in [c.channel_id for c in channels]:
            update_channel(
                archive.channel.channel_id,
                archive.channel.channel_name,
                archive.channel.description,
                archive.channel.header_url,
                archive.channel.avatar_url)
        else:
            insert_channel(
                archive.channel.channel_id,
                archive.channel.channel_name,
                archive.channel.description,
                archive.channel.header_url,
                archive.channel.avatar_url)
            
            
        #動画の追加・更新
        for movie in archive.movie:
            if movie.id in [m.id for m in movies]:
                update_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    movie.view_count,
                    movie.thumbnail_url,
                    'movie'
                )
            else:
                upload_date = get_upload_date(movie.url)
                insert_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    upload_date,
                    movie.view_count,
                    movie.thumbnail_url,
                    'movie'
                )
        #ショートの追加・更新
        for movie in archive.short:
            if movie.id in [m.id for m in movies]:
                update_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    movie.view_count,
                    movie.thumbnail_url,
                    'short'
                )
            else:
                upload_date = get_upload_date(movie.url)
                insert_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    upload_date,
                    movie.view_count,
                    movie.thumbnail_url,
                    'short'
                )
        #ライブの追加・更新
        for movie in archive.live:
            if movie.id in [m.id for m in movies]:
                update_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    movie.view_count,
                    movie.thumbnail_url,
                    'live'
                )
            else:
                upload_date = get_upload_date(movie.url)
                insert_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    upload_date,
                    movie.view_count,
                    movie.thumbnail_url,
                    'live'
                )

"""
データベース用の関数
"""
database = scraper_const.Database()
dbname = database.youtube_path()
def make_database():
    #dbファイル作成
    conn = sqlite3.connect(dbname)
    conn.close()

    #動画のテーブル
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS movie(
                id INTEGER PRIMARY KEY,
                url STRING,
                title STRING,
                date STRING,
                channel_id STRING,
                view_count INTEGER,
                thumbnail_url STRING,
                movie_type STRING
                )
                """)
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()

    #チャンネルのテーブル
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS channel(
                channel_id STRING PRIMARY KEY,
                channel_name STRING,
                description STRING,
                header_url STRING,
                avatar_url STRING
                )
                """)
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()

def search_movie() -> List[scraper_const.MovieInfo]:
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movie")
    results = cursor.fetchall()

    # 接続を閉じる
    conn.close()

    # 結果をまとめる
    records = []
    for row in results:
        rec = scraper_const.MovieInfo(*row)
        records.append(rec)
    
    return records

def search_channel() -> List[scraper_const.ChannelInfo]:
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM channel")
    results = cursor.fetchall()

    # 接続を閉じる
    conn.close()

    # 結果をまとめる
    records = []
    for row in results:
        rec = scraper_const.ChannelInfo(*row)
        records.append(rec)
    
    return records

def insert_movie(
    id:int,
    url:str,
    title:str,
    date:str,
    view_count:int,
    thumbnail_url:str,
    movie_type:str
):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = """
    INSERT INTO movie (id, url, title, date, channel_id, view_count, thumbnail_url, movie_type) 
               VALUES (:id, :url, :title, :date, :channel_id, :view_count, :thumbnail_url, :movie_type)
    """
    args = {
        "id":id,
        "url":url,
        "title":title,
        "date":date,
        "view_count":view_count,
        "thumbnail_url":thumbnail_url,
        "movie_type":movie_type
    }
    
    cursor.execute(query,args)
    conn.commit()
    conn.close()

def insert_channel(
    channel_id:str,
    channel_name:str,
    description:str,
    header_url:str,
    avatar_url:int
):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = """
    INSERT INTO channel (channel_id, channel_name, description, header_url, avatar_url) 
               VALUES (:channel_id, :channel_name, :description, :header_url, :avatar_url)
    """
    args = {
        "channel_id":channel_id,
        "channel_name":channel_name,
        "description":description,
        "header_url":header_url,
        "avatar_url":avatar_url
    }
    
    cursor.execute(query,args)
    conn.commit()
    conn.close()

def update_movie(
    id:int,
    url:str,
    title:str,
    view_count:int,
    thumbnail_url:str,
    movie_type:str
):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = """
    UPDATE movie SET
        url = :url,
        title = :title,
        channel_id = :channel_id,
        view_count = :view_count,
        thumbnail_url = :thumbnail_url,
        movie_type = :movie_type 
    WHERE id = :id
    """
    args = {
        "id":id,
        "url":url,
        "title":title,
        "view_count":view_count,
        "thumbnail_url":thumbnail_url,
        "movie_type":movie_type
    }
    
    cursor.execute(query,args)
    conn.commit()
    conn.close()

def update_channel(
    channel_id:str,
    channel_name:str,
    description:str,
    header_url:str,
    avatar_url:int
):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = """
    UPDATE channel SET
        channel_name = :channel_name,
        description = :description,
        header_url = :header_url,
        avatar_url = :avatar_url 
    WHERE channel_id = :channel_id
    """
    args = {
        "channel_id":channel_id,
        "channel_name":channel_name,
        "description":description,
        "header_url":header_url,
        "avatar_url":avatar_url
    }
    
    cursor.execute(query,args)
    conn.commit()
    conn.close()



    