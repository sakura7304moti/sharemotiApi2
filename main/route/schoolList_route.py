import json
from flask import Blueprint, request, jsonify
import sys
sys.path.append('../')
from src import schoolList, const

#改行文字を取得
NEW_LINE_TEXT = const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('schoolList',__name__)

# schoolListの初期設定
schoolList.init()

"""
SchoolList 学校一覧
"""
@app.route("/schoolList/search", methods=["POST"])
def schoolList_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    records = schoolList.search(word)
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


@app.route("/schoolList/save", methods=["POST"])
def schoolList_save():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    result = schoolList.save(word)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/schoolList/delete", methods=["POST"])
def schoolList_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")

    res = schoolList.delete(word)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response