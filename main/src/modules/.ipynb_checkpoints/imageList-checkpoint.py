"""
画像一覧
"""
from . import const
import sqlite3
import datetime

# sns.dbを作成する
# すでに存在していれば、それにアスセスする。
output = const.Output()
dbname = output.sqlite_db()

"""
CREATE DB
"""
def init():
    conn = sqlite3.connect(dbname)
    # データベースへのコネクションを閉じる。(必須)
    conn.close()
    """
    CREATE TABLE
    """
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    
    # テーブル作成
    cur.execute(
    """CREATE TABLE IF NOT EXISTS imageList2(
        id INTEGER PRIMARY KEY,
        file_name STRING,
        ext STRING,
        title STRING,
        detail STRING,
        create_at STRING,
        update_at STRING
    )
    """
    )
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()
    print('create table imageList2')
    
    #todo DBとフォルダーの画像で一致しないのがあれば更新する
    
"""
INSERT
"""
def insert(file_name:str,ext:str,title:str,detail:str):
    try:
        # 現在の日時を取得
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        query = """
        INSERT INTO imageList2 (file_name , ext , title, detail , create_at, update_at) VALUES 
        (:file_name, :ext ,  :title, :detail, :current_time, :current_time)
        """
        args = {"file_name":file_name,"ext":ext,"title":title,"detail":detail,"current_time":current_time}
        cursor.execute(query, args)

        # データベースへコミット。これで変更が反映される。
        conn.commit()
        conn.close()
        result = const.ImageListStatusResult(True,"")
    except Exception as e:
        print(f'insert err -> {e}')
        result = const.ImageListStatusResult(False,str(e))
    return result
    
"""
UPDATE
更新できるのはタイトルと詳細のみ
"""
def update(id:int,title:str,detail:str):
    try:
        # 現在の日時を取得
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        
        query = """
        UPDATE imageList2 SET title = :title , detail = :detail , update_at = :current_time WHERE id = :id
        """
        
        args={
            'id':id,
            'title':title,
            'detail':detail,
            'current_time':current_time
        }
        cursor.execute(query, args)

        # データベースへコミット。これで変更が反映される。
        conn.commit()
        conn.close()
        result = const.ImageListStatusResult(True,"")
    except Exception as e:
        print(f'update err -> {e}')
        result = const.ImageListStatusResult(False,str(e))
    return result
    
"""
DELETE
"""
def delete(id:int):
    try:
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        query = "DELETE FROM imageList2 WHERE id = :id"
        args = {"id":id}
        # レコードを削除する
        cursor.execute(query, args)

        # 変更をコミットし、接続を閉じる
        conn.commit()
        conn.close()
        
        result = const.ImageListStatusResult(True,"")
    except Exception as e:
        print(f'delete err -> {e}')
        result = const.ImageListStatusResult(False,str(e))
    return result
    
"""
検索
"""
def search():
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    query = "SELECT * FROM imageList2"
    # SELECTクエリを実行
    cursor.execute(query)
    results = cursor.fetchall()
    
    # 結果を表示
    records = []
    for row in results:
        rec = const.ImageListRecord(*row)
        records.append(rec)

    # 接続を閉じる
    conn.close()
    return records