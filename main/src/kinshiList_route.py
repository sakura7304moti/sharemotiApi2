"""
俳句一覧のルーティング
"""
import json
from flask import Blueprint, request, jsonify
from main.src.modules import main_const
from main.src.modules import kinshiList

#改行文字を取得
NEW_LINE_TEXT = main_const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('kinshiList',__name__)

# kinshiListの初期設定
kinshiList.init()


@app.route("/kinshiList/search",methods=["GET"])
def kinshiList_search():
    records = kinshiList.select()
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
        json_data = "{records:[]}"
    response = jsonify(json_data)
    return response

@app.route("/kinshiList/insert",methods=["POST"])
def kinshiList_insert():
    json_data = request.json
    char_name = json_data.get("charName","")
    ssbu_name = json_data.get("ssbuName","")
    desc = json_data.get("desc","")

    result = kinshiList.insert(char_name,ssbu_name,desc)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/kinshiList/update",methods=["POST"])
def kinshiList_update():
    json_data = request.json
    id = int(json_data.get("id",-1))
    char_name = json_data.get("charName","")
    ssbu_name = json_data.get("ssbuName","")
    desc = json_data.get("desc","")

    result = kinshiList.update(id,char_name,ssbu_name,desc)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/kinshiList/delete",methods=["POST"])
def kinshiList_delete():
    json_data = request.json
    id = int(json_data.get("id",-1))
    result = kinshiList.delete(id)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response