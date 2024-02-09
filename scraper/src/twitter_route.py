"""
twitterのルーティング
"""
import json
import math
from flask import Blueprint, request, jsonify
from scraper.src.modules import twitter_sqlite
from scraper.src.modules import scraper_const

#改行文字を取得
NEW_LINE_TEXT = scraper_const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('twitter',__name__)

"""
Monitter Nitter
"""
@app.route("/nitter/search", methods=["POST"])
def nitter_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    # JSONデータから必要なパラメータを抽出
    page_no = json_data.get("page_no", 1)
    page_size = json_data.get("page_size", 40)
    hashtag = json_data.get("hashtag", "")
    start_date = json_data.get("start_date", "")
    end_date = json_data.get("end_date", "")
    user_name = json_data.get("user_name", "")
    mode = json_data.get("mode","")
    min_like = json_data.get("min_like", 0)
    max_like = json_data.get("max_like", 0)

    # search()関数を呼び出し
    records = twitter_sqlite.search(
        page_no, page_size, hashtag, start_date, end_date, user_name,mode, min_like, max_like
    )

    # search_count()関数を呼び出し
    count = twitter_sqlite.search_count(
        hashtag, start_date, end_date, user_name,mode, min_like, max_like
    )
    totalPages = math.ceil(count / page_size)

    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        ),
        "totalPages": totalPages,
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
        json_data = "{'records':[],'totalPages':0}"
    response = jsonify(json_data)
    return response


@app.route("/nitter/search/count", methods=["POST"])
def nitter_search_count_handler():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得

    hashtag = json_data.get("hashtag", "")
    start_date = json_data.get("start_date", "")
    end_date = json_data.get("end_date", "")
    user_name = json_data.get("user_name", "")
    mode = json_data.get("mode","")
    min_like = json_data.get("min_like", 0)
    max_like = json_data.get("max_like", 0)

    # search_count()関数を呼び出し
    count = twitter_sqlite.search_count(
        hashtag, start_date, end_date, user_name,mode, min_like, max_like
    )

    # レスポンスとして結果を返す
    response = jsonify(count=count)
    return response


@app.route("/nitter/hololist", methods=["GET"])
def nitter_get_hololist():
    records = scraper_const.holoList()
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