import json
import os
from flask import Blueprint, flash, jsonify, request, send_file
from PIL import Image
from rembg import remove
import io
import glob
from sub.src.modules import sub_const

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# ファイルアップロードを許可するか判別する
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# tmpに一時保存
def tmp_name(file_name:str):
    return os.path.join(sub_const.get_tmp_dir() , f"cleaned_{file_name}")

# Blueprintのオブジェクトを生成する
app = Blueprint('rembg',__name__)
tm_nm = ''

@app.route('/rembg', methods=['POST'])
def remove_bg():
    #if 'image' not in request.form.keys:
    #    print('Log1')
    #    return {"error": "No image file provided"}, 400

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

    # 画像形式をチェック
    if file and allowed_file(file.filename):
        try:
            input_image = Image.open(file.stream)
        except Exception as e:
            return {"error": str(e)}, 400

    output_image = remove(input_image)

    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    #一時ファイルに保存

    tm_nm = tmp_name(os.path.splitext(file.filename)[0] + '.png')
    print(f"file name {tm_nm}")
    output_image.save(tm_nm)

    return tm_nm

@app.route('/rembg/download', methods=['GET'])
def remove_file_download():
    fileName = request.args.get('fileName','')
    path = os.path.join(sub_const.get_tmp_dir(), fileName)
    return send_file(path, mimetype='image/png')