"""
スマブラのクリップ一覧
"""
import os
import glob

from . import file_const

DATA_PATH = file_const.get_data_path()

"""
クリップの一覧を取得
"""
def search():
    path_list = glob.glob(os.path.join(DATA_PATH,'ssbu','*','*','*.mp4'))
    records = []
    for path in path_list:
        id = path_list.index(path)
        file_name = os.path.basename(path).split('.')[0]
        dir_path = os.path.dirname(path)
        date = os.path.basename(dir_path)
        dir_path_u = os.path.dirname(dir_path)
        year = os.path.basename(dir_path_u)
        rec = file_const.ssbuListRecord(id,file_name,date,year)
        records.append(rec)
    return records

"""
IDをもとに動画の要素を取得
"""
def select(select_id:int):
    path_list = glob.glob(os.path.join(DATA_PATH,'ssbu','*','*','*.mp4'))
    for path in path_list:
        id = path_list.index(path)
        if id == select_id:
            file_name = os.path.basename(path).split('.')[0]
            dir_path = os.path.dirname(path)
            date = os.path.basename(dir_path)
            dir_path_u = os.path.dirname(dir_path)
            year = os.path.basename(dir_path_u)
            rec = file_const.ssbuListRecord(id,file_name,date,year)
            break
    return rec