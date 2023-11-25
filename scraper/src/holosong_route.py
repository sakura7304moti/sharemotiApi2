"""
ホロライブのオリ曲や歌っていたのルーティング
"""
import json
from flask import Blueprint, jsonify
from scraper.src.modules import holosong
from scraper.src.modules import scraper_const

#改行文字を取得
NEW_LINE_TEXT = scraper_const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('holosong',__name__)
@app.route("/holoSong/search",methods=["GET"])
def holosong_select():
    records = holosong.get_cover_songs()
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

@app.route("/holoSong/hololist", methods=["GET"])
def holosong_get_hololist():
    json_data = json.dumps(scraper_const.holoMember(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
ホロライブのオリキョクを取得する
"""
@app.route('/holoSong/ori',methods=["GET"])
def holosong_ori():
    records = holosong.get_original_songs()
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