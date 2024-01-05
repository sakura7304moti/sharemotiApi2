import os
import pandas as pd
import yaml
import glob
import json
import datetime

# プロジェクトの相対パス
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# 各保存先
class Output:
    def __init__(self):
        self._base_path = base_path

    def sqlite_db(self):
        return os.path.join(self._base_path, "share.db")
    
    def image_upload_folder(self):
        return os.path.join(self._base_path,'uploads')

# 空文字用の定数
def get_new_line_text() -> str:
    return "jsdlkjflasjfiojadispfosdjfposdj"

"""
options
"""


def ssbu_names():
    df = pd.read_csv(os.path.join(base_path, "option", "ssbu.csv"))
    records = []
    for index, row in df.iterrows():
        name = row["name"]
        url = row["url"]
        rec = SsbuNameRecord(name,url)
        records.append(rec)
    return records


def ssbu_dict():
    df = pd.read_csv(os.path.join(base_path, "option", "ssbu_dict.csv"))
    return df

def img_dir():
    dir_name = os.path.join(base_path,'img')
    os.makedirs(dir_name,exist_ok=True)
    return dir_name


"""
Record interface
""" 
class WordList2Record:  # 名言集2
    def __init__(self, word: str, desc: str,createAt:str,updateAt:str):
        self.word = word
        self.desc = desc
        self.createAt = datetime.datetime.strptime(createAt,'%Y-%m-%d %H:%M:%S')
        self.updateAt = datetime.datetime.strptime(updateAt,'%Y-%m-%d %H:%M:%S')

    def __dict__(self):
        return {"word": self.word, "desc": self.desc,"createAt":self.createAt.strftime('%Y-%m-%d %H:%M:%S'),"updateAt":self.updateAt.strftime('%Y-%m-%d %H:%M:%S')}


class NameListRecord:  # あだ名集
    def __init__(self, key: str, val: str):
        self.key = key
        self.val = val

    def __dict__(self):
        return {"key": self.key, "val": self.val}
    

class YakiListRecord:  # 焼き直し条約
    def __init__(self, word: str, yaki: str):
        self.word = word
        self.yaki = yaki

    def __dict__(self):
        return {"word": self.word, "yaki": self.yaki}
    
class SchoolListRecord:  # 学校一覧
    def __init__(self, word: str):
        self.word = word

    def __dict__(self):
        return {"word": self.word}
    
class MannerListRecord:  # 日本国失礼憲法
    def __init__(self, word: str):
        self.word = word

    def __dict__(self):
        return {"word": self.word}
    
class HaikuListRecord:#俳句一覧
    def __init__(self,id:int,first:str,second:str,third:str,poster:str,detail:str,createAt:str,updateAt:str):
        self.id = id
        self.first = first
        self.second = second
        self.third = third
        self.detail = detail
        self.poster = poster
        self.createAt = datetime.datetime.strptime(createAt,'%Y-%m-%d %H:%M:%S')
        self.updateAt = datetime.datetime.strptime(updateAt,'%Y-%m-%d %H:%M:%S')

    def __dict__(self):
        return {"id":self.id,"first":self.first,"second":self.second,"third":self.third,"poster":self.poster,"detail":self.detail,"createAt":self.createAt.strftime('%Y-%m-%d %H:%M:%S'),"updateAt":self.updateAt.strftime('%Y-%m-%d %H:%M:%S')}

class HaikuListStatusResult:#俳句一覧の追加結果
    def __init__(self,success:bool,errorText:str):
        self.success = success
        self.errorText = errorText
    
    def __dict__(self):
        return {"success":self.success,"errorText":self.errorText}
    
class ImageListRecord:#画像一覧
    def __init__(self,
                 id:int,
                 file_name:str,
                 ext:str,
                 title:str,
                 detail:str,
                 create_at:str,
                 update_at:str):
        self.id = id
        self.file_name = file_name
        self.ext = ext
        self.title = title
        self.detail = detail
        self.create_at = datetime.datetime.strptime(create_at,'%Y-%m-%d %H:%M:%S')
        self.update_at = datetime.datetime.strptime(update_at,'%Y-%m-%d %H:%M:%S')
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name,"ext":self.ext, "title":self.title,"detail":self.detail,"createAt":self.create_at.strftime('%Y-%m-%d %H:%M:%S'),"updateAt":self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
    def __str__(self):
        return f"ImageListRecord(id={self.id}, file_name={self.file_name},ext={self.ext}, title={self.title}, " \
               f"detail={self.detail}, create_at={self.create_at}, update_at={self.update_at})"

    
class ImageListStatusResult:#画像の追加結果
    def __init__(self,success:bool,errorText:str):
        self.success = success
        self.errorText = errorText
    
    def __dict__(self):
        return {"success":self.success,"errorText":self.errorText}
    
class SsbuNameRecord:#スマブラのキャラ名と画像URL
    def __init__(self,name:str,url:str):
        self.name = name
        self.url = url
    def __dict__(self):
        return {"name":self.name,"url":self.url}

class KinshiListRecord:  # 禁止キャラ一覧
    def __init__(self,id:int, char_name: str, ssbu_name: str,  desc: str,createAt:str,updateAt:str):
        self.id = id
        self.char_name = char_name
        self.ssbu_name = ssbu_name
        self.desc = desc
        self.createAt = datetime.datetime.strptime(createAt,'%Y-%m-%d %H:%M:%S')
        self.updateAt = datetime.datetime.strptime(updateAt,'%Y-%m-%d %H:%M:%S')

    def __dict__(self):
        return {"id":self.id, "charName": self.char_name, "ssbuName":self.ssbu_name, "desc": self.desc,"createAt":self.createAt.strftime('%Y-%m-%d %H:%M:%S'),"updateAt":self.updateAt.strftime('%Y-%m-%d %H:%M:%S')}