"""
ホロライブのアーカイブのスクレイピング
"""
import json
from flask import Blueprint, jsonify, request
from scraper.src.modules import holo_archive
from scraper.src.modules import scraper_const

#改行文字を取得
NEW_LINE_TEXT = scraper_const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('holoarchive',__name__)

"""
チャンネル情報の一覧
"""
@app.route("/holoArchive/search/channel",methods=["GET"])
def holomovie_channel():
    records = holo_archive.search_channel()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace('"[{', "[{").replace('}]"', "}]")
    
    #改行文字だけ残してバックスラッシュは削除
    json_data = json_data.replace('\\n',NEW_LINE_TEXT)
    json_data = json_data.replace('\\','')
    json_data = json_data.replace(NEW_LINE_TEXT,'\\n')
    
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

"""
動画情報の一覧
"""
@app.route("/holoArchive/search/movie",methods=["POST"])
def holomovie_movie():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    # JSONデータから必要なパラメータを抽出
    page_no = json_data.get("pageNo", 1)
    page_size = json_data.get("pageSize", 20)
    title = json_data.get("title", "")
    from_date = json_data.get("fromDate", "")
    to_date = json_data.get("toDate", "")
    channel_id = json_data.get("channelId", "")
    movie_type = json_data.get("movieType","")

    
    records = holo_archive.search_movie(
        page_no,page_size,
        title,
        from_date,to_date,
        channel_id,
        movie_type
    )
    total_pages = holo_archive.search_movie_count(
        page_size,
        title,
        from_date,to_date,
        channel_id,
        movie_type
    )
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        ),
        "totalPages": total_pages
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace('"[{', "[{").replace('}]"', "}]")
    
    #改行文字だけ残してバックスラッシュは削除
    json_data = json_data.replace('\\n',NEW_LINE_TEXT)
    json_data = json_data.replace('\\','')
    json_data = json_data.replace(NEW_LINE_TEXT,'\\n')
    
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

"""
チャンネルURLの一覧
"""
@app.route("/holoArchive/channelUrl",methods=["GET"])
def holochannel():
    records = scraper_const.channel_list()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace('"[{', "[{").replace('}]"', "}]").replace('"[', "[").replace(']"', "]")
    
    #改行文字だけ残してバックスラッシュは削除
    json_data = json_data.replace('\\n',NEW_LINE_TEXT)
    json_data = json_data.replace('\\','')
    json_data = json_data.replace(NEW_LINE_TEXT,'\\n')
    
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response