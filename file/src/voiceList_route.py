"""
ボイス一覧のルーティング
"""
import json
import os
from flask import Blueprint, request, jsonify, send_file
from file.src.modules import file_const
from file.src.modules import voiceList

#改行文字を取得
NEW_LINE_TEXT = file_const.get_new_line_text()

#保存先
DATA_PATH = file_const.get_data_path()

# Blueprintのオブジェクトを生成する
app = Blueprint('voiceList',__name__)

@app.route("/voice/search",methods=['GET'])
def voicelist_search():
    records = voiceList.search()
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

@app.route('/voice/download',methods=['GET'])
def voicelist_download():
    id = int(request.args.get('id',-1))
    rec = voiceList.select(id)
    path = os.path.join(DATA_PATH,'ボイス',rec.file_name+'.mp3')
    return send_file(path , mimetype='audio/mpeg')
