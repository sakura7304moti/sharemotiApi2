from typing import List
import yt_dlp
from tqdm import tqdm
from . import scraper_const

channel_url_list = scraper_const.channel_list()


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
    return scraper_const.ChannelInfo(channel_name,description,header_url,avatar_url)

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
    for index,rec in enumerate(entries):
        info = get_movie_info(rec)
        if info is not None:
            movie_index = abs(index - len(entries))
            movie_info = scraper_const.MovieInfo(movie_index,*info)
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

def holo_archives() -> List[scraper_const.Archive]:
    archives = []
    for url in tqdm(channel_url_list,desc="get archives"):
        archive = inferece_channenl(url)
        archives.append(archive)
    return archives