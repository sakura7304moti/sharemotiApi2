import json
from flask import Blueprint, request, jsonify
import sys
sys.path.append('../')
from src import mannerList, const

#改行文字を取得
NEW_LINE_TEXT = const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('mannerList',__name__)

# mannerListの初期設定
mannerList.init()

"""
MannerList 日本国失礼憲法
"""
@app.route("/mannerList/search", methods=["POST"])
def mannerList_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    records = mannerList.search(word)
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


@app.route("/mannerList/save", methods=["POST"])
def mannerList_save():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    result = mannerList.save(word)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/mannerList/delete", methods=["POST"])
def mannerList_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    res = mannerList.delete(word)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response