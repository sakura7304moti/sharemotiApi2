import yt_dlp

def get_playlist_urls(playlist_url:str):
    # yt-dlpのオプション設定
    ydl_opts = {
        'quiet': True,  # 出力を最小限に抑える
        'extract_flat': True,  # プレイリストの情報のみを取得し、動画をダウンロードしない
    }

    video_urls = []  # 動画のURLを格納するリスト

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # プレイリストの情報を取得
        info_dict = ydl.extract_info(playlist_url, download=False)
        # プレイリスト内の各動画に対して
        for entry in info_dict['entries']:
            # 動画のURLをリストに追加
            video_urls.append(entry['url'])

    return video_urls

def search():
    url = 'https://www.youtube.com/playlist?list=PLbP5km9K7tgfHKxHvk9nOx7hcbLbnHSuS'
    return get_playlist_urls(url)