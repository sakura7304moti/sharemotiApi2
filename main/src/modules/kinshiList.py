"""
禁止キャラ一覧
"""
from . import main_const
import sqlite3
import datetime

# sns.dbを作成する
# すでに存在していれば、それにアスセスする。
output = main_const.Output()
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
        """CREATE TABLE IF NOT EXISTS kinshiList(
                id INTEGER PRIMARY KEY,
                char_name STRING,
                ssbu_name STRING,
                desc STRING,
                create_at STRING,
                update_at STRING
                )
                """
    )

    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()

"""
INSERT and UPDATE
"""

def insert(char_name:str, ssbu_name:str, desc:str):
    try:
        # 現在の日時を取得
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        query = "INSERT INTO kinshiList (char_name, ssbu_name,desc,create_at,update_at) VALUES (:char_name, :ssbu_name, :desc, :current_time, :current_time)"
        args = {"char_name": char_name, "ssbu_name": ssbu_name,"desc":desc,"current_time":current_time}
        cursor.execute(query, args)

        # データベースへコミット。これで変更が反映される。
        conn.commit()
        conn.close()
        result = main_const.HaikuListStatusResult(True,"")
    except Exception as e:
        #エラー出たらエラー内容と追加失敗を返す
        result = main_const.HaikuListStatusResult(False,str(e))
    return result

def update(id:int,char_name:str, ssbu_name:str, desc:str):
    try:
        # 現在の日時を取得
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        query = """
        UPDATE kinshiList SET 
        char_name = :char_name, 
        ssbu_name = :ssbu_name, 
        desc = :desc, 
        update_at = :current_time 
        WHERE id = :id
        """

        args = {
            'id':id,
            'char_name':char_name,
            'ssbu_name':ssbu_name,
            'desc':desc,
            'current_time':current_time
        }
        cursor.execute(query, args)

        # データベースへコミット。これで変更が反映される。
        conn.commit()
        conn.close()
        result = main_const.HaikuListStatusResult(True,"")
    except Exception as e:
        #エラー出たらエラー内容と追加失敗を返す
        result = main_const.HaikuListStatusResult(False,str(e))
    return result

"""
DELETE
"""
def delete(id:int):
    try:
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        query = "DELETE FROM kinshiList WHERE id = :id"
        args = {"id":id}

        # レコードを削除する
        cursor.execute(query, args)

        # 変更をコミットし、接続を閉じる
        conn.commit()
        conn.close()

        result = main_const.HaikuListStatusResult(True,"")
    except Exception as e:
        #エラー出たらエラー内容と追加失敗を返す
        result = main_const.HaikuListStatusResult(False,str(e))
    return result

"""
SELECT
"""
def select() -> list[main_const.KinshiListRecord]:
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    args = {}
    query = "SELECT * FROM kinshiList"
    
    # SELECTクエリを実行
    cursor.execute(query)
    results = cursor.fetchall()

    # 結果を表示
    records = []
    for row in results:
        rec = main_const.KinshiListRecord(*row)
        records.append(rec)

    # 接続を閉じる
    conn.close()
    return records