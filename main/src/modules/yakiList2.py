"""
焼き直し条約2 API
"""
from . import main_const
import sqlite3
import datetime

output = main_const.Output()


# sns.dbを作成する
# すでに存在していれば、それにアスセスする。
dbname = output.sqlite_db()

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
    cur.execute(
        """CREATE TABLE IF NOT EXISTS yakiList2(
                id INTEGER PRIMARY KEY,
                word STRING,
                yaki STRING,
                create_at STRING,
                update_at STRING
                )
                """
    )
    
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()

def exists(
    word:str,
    yaki:str
):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = "SELECT * FROM yakiList2 where word = :word and yaki = :yaki"
    args = {
        "word":word,
        "yaki":yaki
    }

    #検索
    cursor.execute(query,args)
    results = cursor.fetchall()

    #閉じる
    conn.close()

    return len(results) > 0
    

def insert(
    word:str,
    yaki:str
):
    try:
        if not exists(word,yaki):
            # データベースに接続する
            conn = sqlite3.connect(dbname)
            cursor = conn.cursor()
        
            # 現在の日時を取得
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
            query = "INSERT INTO yakiList2 (word, yaki, create_at, update_at) VALUES (:word, :yaki, :create_at, :update_at)"
            args = {"word": word, "yaki" : yaki, "create_at" : current_time, "update_at" : current_time}
    
            cursor.execute(query, args)
    
            # 変更をコミットし、接続を閉じる
            conn.commit()
            conn.close()
            return main_const.DbResult(True,"")

    except Exception as e:
        err_text = str(e)
        return main_const.DbResult(False,err_text)
        
def update(
    id:int,
    word:str,
    yaki:str
):
    try:
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
    
        # 現在の日時を取得
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = """
            UPDATE yakiList2 Set 
                word = :word, 
                yaki = :yaki, 
                update_at = :current_time
            WHERE id = :id
        """
        args = {
            "id" : id,
            "word" : word,
            "yaki" : yaki,
            "current_time" : current_time
        }

        cursor.execute(query, args)
        # 変更をコミットし、接続を閉じる
        conn.commit()
        conn.close()
        return main_const.DbResult(True,"")

    except Exception as e:
        err_text = str(e)
        return main_const.DbResult(False,err_text)

def delete(id:int):
    try:
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
    
        query = "DELETE FROM yakiList2 WHERE id = :id"
        args = {"id" : id}
    
        # レコードを削除する
        cursor.execute(query, args)
    
        # 変更をコミットし、接続を閉じる
        conn.commit()
        conn.close()
        return main_const.DbResult(True,"")

    except Exception as e:
        err_text = str(e)
        return main_const.DbResult(False,err_text)

def search():
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = "SELECT * FROM yakiList2"
    
    # SELECTクエリを実行
    cursor.execute(query)
    results = cursor.fetchall()

    # 結果を表示
    records = []
    for row in results:
        rec = main_const.YakiList2Record(*row)
        records.append(rec)

    # 接続を閉じる
    conn.close()
    return records