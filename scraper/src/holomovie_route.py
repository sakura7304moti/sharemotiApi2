"""
ホロライブの記念配信のスクレイピング
"""
import json
from flask import Blueprint, jsonify
from scraper.src.modules import holosong
from scraper.src.modules import scraper_const

#改行文字を取得
NEW_LINE_TEXT = scraper_const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('holomovie',__name__)
@app.route("/holoMovie/memory",methods=["GET"])
def holomovie_memory():
    records = holosong.get_memory_movies()
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