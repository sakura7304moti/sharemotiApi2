"""
完成品一覧のルーティング
"""
import json
import os
from flask import Blueprint, request, jsonify, send_file
from file.src.modules import file_const
from file.src.modules import movieList

#改行文字を取得
NEW_LINE_TEXT = file_const.get_new_line_text()

#保存先
DATA_PATH = file_const.get_data_path()

# Blueprintのオブジェクトを生成する
app = Blueprint('movieList',__name__)

@app.route("/movieList/search",methods=['GET'])
def movielist_search():
    records = movieList.search()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

@app.route('/movieList/download',methods=['GET'])
def movielist_download():
    poster = request.args.get('poster',"")
    file_name = request.args.get('fileName',"")
    path = os.path.join(DATA_PATH,'movie',rec.poster,rec.file_name+'.mp4')
    return send_file(path , mimetype='video/mp4')