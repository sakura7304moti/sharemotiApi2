import os
import pandas as pd
import yaml
import glob
import json
import datetime
"""
Functions
"""

# プロジェクトの相対パス
_base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 空文字用の定数
def get_new_line_text() -> str:
    return "jsdlkjflasjfiojadispfosdjfposdj"

# dataのパス
def get_data_path() -> str:
    return os.path.join(_base_path,'data')

"""
Record interface
"""
class KaraokeListRecord:#カラオケ音声の一覧
    def __init__(self,
                 id:int,
                 file_name:str,
                 date:str):
        self.id = id
        self.file_name = file_name
        self.date = date
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name,"date":self.date}
    def __str__(self):
        return f"ID: {self.id}, File Name: {self.file_name}, Date: {self.date}"

class VoiceListRecord:#ボイス
    def __init__(self,
                 id:int,
                 file_name:str):
        self.id = id
        self.file_name = file_name
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name}
    def __str__(self):
        return f"ID: {self.id}, File Name: {self.file_name}"
    
class RadioListRecord:#ラジオの一覧
    def __init__(self,
                 id:int,
                 file_name:str,
                 date:str):
        self.id = id
        self.file_name = file_name
        self.date = date
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name,"date":self.date}
    def __str__(self):
        return f"ID: {self.id}, File Name: {self.file_name}, Date: {self.date}"
    
class ssbuListRecord:#スマブラのクリップ
    def __init__(self,
                 id:int,
                 file_name:str,
                 date:str,
                 year:str):
        self.id = id
        self.file_name = file_name
        self.date = date
        self.year = year
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name,"date":self.date,"year":self.year}
    def __str__(self):
        return f"ID: {self.id}, File Name: {self.file_name}, Date: {self.date}, Year: {self.year}"
    
class SsbuNameRecord:#スマブラのキャラ名と画像URL
    def __init__(self,name:str,url:str):
        self.name = name
        self.url = url
    def __dict__(self):
        return {"name":self.name,"url":self.url}

class MovieListRecord:#完成品
    def __init__(self,
                 id:int,
                 file_name:str,
                 poster:str):
        self.id = id
        self.file_name = file_name
        self.poster = poster
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name,"poster":self.poster}
    def __str__(self):
        return f"ID: {self.id}, File Name: {self.file_name}, Poster: {self.poster}"