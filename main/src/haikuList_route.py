"""
俳句一覧のルーティング
"""
import json
from flask import Blueprint, request, jsonify
from main.src.modules import main_const
from main.src.modules import haikuList

#改行文字を取得
NEW_LINE_TEXT = main_const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('haikuList',__name__)

# haikuListの初期設定
haikuList.init()


@app.route("/haikuList/search",methods=["POST"])
def haikuList_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    id = int(json_data.get("id","-1"))
    haikuText = json_data.get("haikuText","")
    poster = json_data.get("poster","")
    detail = json_data.get("detail","")

    records = haikuList.select(id,haikuText,poster,detail)
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

@app.route("/haikuList/insert",methods=["POST"])
def haikuList_insert():
    json_data = request.json
    first = json_data.get("first","")
    second = json_data.get("second","")
    third = json_data.get("third","")
    poster = json_data.get("poster","")
    detail = json_data.get("detail","")

    result = haikuList.insert(first,second,third,poster,detail)
    print(result.__dict__)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/haikuList/update",methods=["POST"])
def haikuList_update():
    json_data = request.json
    id = int(json_data.get("id",-1))
    first = json_data.get("first","")
    second = json_data.get("second","")
    third = json_data.get("third","")
    poster = json_data.get("poster","")
    detail = json_data.get("detail","")

    result = haikuList.update(id,first,second,third,poster,detail)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/haikuList/delete",methods=["POST"])
def haikuList_delete():
    json_data = request.json
    id = int(json_data.get("id",-1))
    result = haikuList.delete(id)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response