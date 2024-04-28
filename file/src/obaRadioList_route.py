"""
おばあちゃんレイディオのルーティング
"""
import json
import os
from flask import Blueprint, request, jsonify, send_file
from file.src.modules import file_const
from file.src.modules import obaRadioList

# Blueprintのオブジェクトを生成する
app = Blueprint('obaRadioList',__name__)

@app.route("/obaradio/search",methods=['GET'])
def oba_radio_search():
    records = obaRadioList.search()
    json_date = str(records)
    
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response