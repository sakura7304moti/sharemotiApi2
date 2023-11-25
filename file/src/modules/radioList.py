"""
ラジオの一覧
"""
import os
import glob
import datetime

from . import file_const

DATA_PATH = file_const.get_data_path()


"""
音声の一覧を取得
"""
def search():
    path_list = glob.glob(os.path.join(DATA_PATH,'radio','mp3','*.mp3'))
    records = []
    for path in path_list:
        id = path_list.index(path)
        file_name,ext = os.path.splitext(os.path.basename(path))
        date = ''
        try:
            split_text = file_name.split(' ')
            date_text = split_text[-2]
            time_text = split_text[-1]
            date = f'{date_text} {time_text}'
        except:
            pass

        rec = file_const.RadioListRecord(id,file_name,date)
        records.append(rec)
    # 日付文字列を日付オブジェクトに変換してソート
    #records = sorted(records, key=lambda x: datetime.datetime.strptime(x.date, '%Y-%m-%d %H:%M:%S'))

    return records

"""
IDをもとに動画の要素を取得
"""
def select(select_id:int):
    path_list = glob.glob(os.path.join(DATA_PATH,'radio','mp3','*.mp3'))
    for path in path_list:
        id = path_list.index(path)
        if id == select_id:
            file_name,ext = os.path.splitext(os.path.basename(path))
            date = ''
            try:
                split_text = file_name.split(' ')
                date_text = split_text[-2]
                time_text = split_text[-1]
                date = f'{date_text} {time_text}'
            except:
                pass

            rec = file_const.RadioListRecord(id,file_name,date)
            print(rec)
            break
    return rec