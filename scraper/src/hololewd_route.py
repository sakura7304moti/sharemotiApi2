"""
ホロライブのエロ画像のスクレイピング
"""
import json
import math

from flask import Blueprint, jsonify, request
from scraper.src.modules import hololewd_sqlite
from scraper.src.modules import scraper_const

# Blueprintのオブジェクトを生成する
app = Blueprint('hololewd',__name__)

@app.route("/hololewd/search",methods=["POST"])
def hololewd_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    # JSONデータから必要なパラメータを抽出
    page_no = json_data.get("pageNo", 1)
    page_size = json_data.get("pageSize", 20)
    flair_text = json_data.get("flairText", "")
    min_score = json_data.get("minScore", 50)

    records , count = hololewd_sqlite.search(
        page_no,
        page_size,
        flair_text,
        min_score
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
    json_data = json_data.replace('\\','')
    
    if len(records) == 0:
        json_data = "{'records':[],'totalPages':0}"
    response = jsonify(json_data)
    return response

@app.route("/hololewd/hololist",methods=["GET"])
def hololewd_hololist():
    json_data = json.dumps(scraper_const.hololewd_flair_texts(), ensure_ascii=False)
    response = jsonify(json_data)
    return response
    