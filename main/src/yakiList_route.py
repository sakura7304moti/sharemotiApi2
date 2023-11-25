"""
焼き直し条約のルーティング
"""
import json
from flask import Blueprint, request, jsonify
from main.src.modules import main_const
from main.src.modules import yakiList

#改行文字を取得
NEW_LINE_TEXT = main_const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('yakiList',__name__)

# yakiListの初期設定
yakiList.init()

@app.route("/yakiList/search", methods=["POST"])
def yakiList_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    text = json_data.get("text", "")

    records = yakiList.search(text)
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


@app.route("/yakiList/save", methods=["POST"])
def yakiList_save():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    yaki = json_data.get("yaki", "")

    result = yakiList.save(word, yaki)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/yakiList/delete", methods=["POST"])
def yakiList_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    yaki = json_data.get("yaki", "")

    res = yakiList.delete(word, yaki)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response