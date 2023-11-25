"""
画像一覧のルーティング
"""
import datetime
import json
import os
from flask import Blueprint, flash, request, jsonify, send_file
from werkzeug.utils import secure_filename
from main.src.modules import main_const
from main.src.modules import imageList


#改行文字を取得
NEW_LINE_TEXT = main_const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('imageList',__name__)

# imageListの初期設定
imageList.init()

# 保存先のフォルダーを取得・作成
output = main_const.Output()
UPLOAD_FOLDER = output.image_upload_folder()
print(f'uploads -> {UPLOAD_FOLDER}')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# ファイルアップロードを許可するか判別する
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/imageList/insert',methods=['POST'])
def imagelist_insert():
    json_data = request.json
    file_name = json_data.get("fileName","")
    ext = json_data.get("ext","")
    title = json_data.get("title","")
    detail = json_data.get("detail","")
    
    result = imageList.insert(file_name,ext,title,detail)
    
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response
    
@app.route('/imageList/upload', methods=['GET', 'POST'])
def imagelist_upload():
    # check if the post request has the file part
    print(request.files)
    if 'file' not in request.files:
        flash('No file part')
        jsondata = {"fileName":''}
        response = jsonify(jsondata)
        return response
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        print('No selected file')
        jsondata = {"fileName":''}
        response = jsonify(jsondata)
        return response

    #ext ok filename ok
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[-1].lower()
        
        # 現在の日時を取得
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y%m%d%H%M%S")
        save_file_name = formatted_datetime + '.' + ext
        
        file.save(os.path.join(UPLOAD_FOLDER, save_file_name))
        
        jsondata = {"fileName":save_file_name}
        response = jsonify(jsondata)
        return response
        
@app.route('/imageList/download',methods=['GET'])
def imagelist_download():
    #image file only
    file_name = request.args.get('fileName')
    ext = request.args.get('ext')
    
    path = os.path.join(UPLOAD_FOLDER,file_name+'.'+ext)
    print(f'download path -> {path}')
    return send_file(path, mimetype='image/jpeg')

@app.route("/imageList/search",methods=['GET'])
def imagelist_search():
    records = imageList.search()
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

@app.route("/imageList/update",methods=["POST"])
def imagelist_update():
    json_data = request.json
    id = json_data.get("id",-1)
    title = json_data.get("title","")
    detail = json_data.get("detail","")
    
    result = imageList.update(id,title,detail)
    
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/imageList/delete",methods=["POST"])
def imagelist_delete():
    json_data = request.json
    id = json_data.get("id",-1)
    
    result = imageList.delete(id)
    
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response