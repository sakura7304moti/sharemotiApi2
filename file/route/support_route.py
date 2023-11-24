"""
その他のルーティング
"""
from flask import Blueprint, request, send_file
import urllib

# Blueprintのオブジェクトを生成する
app = Blueprint('support',__name__)

@app.route("/support/download_image",methods=["GET"])
def download_image():
    image_url = request.args.get('url')
    try:
        req = urllib.request.Request(image_url)
        req.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0")
        image_response = urllib.request.urlopen(req)
        return send_file(image_response, mimetype='image/jpeg')
    except Exception as e:
        return str(e), 400