"""
焼き直し条約2のルーティング
"""
import json
from flask import Blueprint, request, jsonify
from main.src.modules import main_const
from main.src.modules import yakiList2

#改行文字を取得
NEW_LINE_TEXT = main_const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('yakiList2',__name__)

# nameListの初期設定
yakiList2.init()

@app.route("/yakiList2/search", methods=["GET"])
def yakiList2_search():
    records = yakiList2.search()
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

@app.route("/yakiList2/insert", methods=["POST"])
def yakiList2_insert():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    yaki = json_data.get("yaki", "")

    result = yakiList2.insert(word, yaki)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/yakiList2/update", methods=["POST"])
def yakiList2_update():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    id = int(json_data.get("id","-1"))
    word = json_data.get("word", "")
    yaki = json_data.get("yaki", "")

    result = yakiList2.update(id, word, yaki)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/yakiList2/delete", methods=["POST"])
def yakiList2_delete():
    json_data = request.json
    id = int(json_data.get("id",-1))
    result = yakiList2.delete(id)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response