"""
あだ名一覧2 API
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
        """CREATE TABLE IF NOT EXISTS nameList2(
                id INTEGER PRIMARY KEY,
                name STRING,
                ssbu_name STRING,
                create_at STRING,
                update_at STRING
                )
                """
    )
    
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()

def exists(
    name:str,
    ssbu_name:str
):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = "SELECT * FROM nameList2 where name = :name and ssbu_name = :ssbu_name"
    args = {
        "name":name,
        "ssbu_name":ssbu_name
    }

    #検索
    cursor.execute(query,args)
    results = cursor.fetchall()

    #閉じる
    conn.close()

    return len(results) > 0
    

def insert(
    name:str,
    ssbu_name:str
):
    try:
        if not exists(name,ssbu_name):
            # データベースに接続する
            conn = sqlite3.connect(dbname)
            cursor = conn.cursor()
        
            # 現在の日時を取得
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
            query = "INSERT INTO nameList2 (name, ssbu_name, create_at, update_at) VALUES (:name, :ssbu_name, :create_at, :update_at)"
            args = {"name": name, "ssbu_name" : ssbu_name, "create_at" : current_time, "update_at" : current_time}
    
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
    name:str,
    ssbu_name:str
):
    try:
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
    
        # 現在の日時を取得
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = """
            UPDATE nameList2 Set 
                name = :name, 
                ssbu_name = :ssbu_name, 
                update_at = :current_time
            WHERE id = :id
        """
        args = {
            "id" : id,
            "name" : name,
            "ssbu_name" : ssbu_name,
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
    
        query = "DELETE FROM nameList2 WHERE id = :id"
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

    query = "SELECT * FROM nameList2"
    
    # SELECTクエリを実行
    cursor.execute(query)
    results = cursor.fetchall()

    # 結果を表示
    records = []
    for row in results:
        rec = main_const.NameList2Record(*row)
        records.append(rec)

    # 接続を閉じる
    conn.close()
    return records