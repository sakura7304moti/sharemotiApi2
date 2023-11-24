import json
from flask import Blueprint, request, jsonify
import sys
sys.path.append('../')
from src import wordList2, const

#改行文字を取得
NEW_LINE_TEXT = const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('wordList2',__name__)

# wordList2の初期設定
wordList2.init()

"""
WordList2 名言集2
"""
@app.route("/wordList2/search", methods=["POST"])
def wordlist2_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    text = json_data.get("text", "")

    records = wordList2.search(text)
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


@app.route("/wordList2/save", methods=["POST"])
def wordlist2_save():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    desc = json_data.get("desc", "")

    result = wordList2.save(word, desc)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/wordList2/delete", methods=["POST"])
def wordlist2_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    word = json_data.get("word", "")
    desc = json_data.get("desc", "")

    res = wordList2.delete(word, desc)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response