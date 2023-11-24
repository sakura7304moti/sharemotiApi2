"""
カラオケ動画の一覧
"""
import os
import glob

from . import const

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))# プロジェクトの相対パス


"""
音声の一覧を取得
"""
def search():
    path_list = glob.glob(os.path.join(base_path,'data','karaoke','*','*.mp3'))
    records = []
    for path in path_list:
        id = path_list.index(path)
        file_name = os.path.basename(path).split('.')[0]
        dir_path = os.path.dirname(path)
        date = os.path.basename(dir_path)

        rec = const.KaraokeListRecord(id,file_name,date)
        records.append(rec)
    return records

"""
IDをもとに動画の要素を取得
"""
def select(select_id:int):
    path_list = glob.glob(os.path.join(base_path,'data','karaoke','*','*.mp3'))
    for path in path_list:
        id = path_list.index(path)
        if id == select_id:
            file_name = os.path.basename(path).split('.')[0]
            dir_path = os.path.dirname(path)
            date = os.path.basename(dir_path)
            rec = const.KaraokeListRecord(id,file_name,date)
            print(rec)
            break
    return rec