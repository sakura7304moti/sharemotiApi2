"""
俳句一覧
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
        """CREATE TABLE IF NOT EXISTS haikuList(
                id INTEGER PRIMARY KEY,
                first STRING,
                second STRING,
                third STRING,
                poster STRING,
                detail STRING,
                create_at STRING,
                update_at STRING
                )
                """
    )

    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()
    print('create table haikuList')

"""
INSERT and UPDATE
"""

def insert(first:str,second:str,third:str,poster:str,detail:str):
    try:
        # 現在の日時を取得
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        query = "INSERT INTO haikuList (first, second,third,poster,detail,create_at,update_at) VALUES (:first, :second, :third, :poster, :detail, :current_time, :current_time)"
        args = {"first": first, "second": second,"third":third,"poster":poster,"detail":detail,"current_time":current_time}
        cursor.execute(query, args)

        # データベースへコミット。これで変更が反映される。
        conn.commit()
        conn.close()
        result = main_const.HaikuListStatusResult(True,"")
    except Exception as e:
        #エラー出たらエラー内容と追加失敗を返す
        result = main_const.HaikuListStatusResult(False,str(e))
    return result

def update(id:int,first:str,second:str,third:str,poster:str,detail:str):
    try:
        # 現在の日時を取得
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # データベースに接続する
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        query = """
        UPDATE haikuList SET 
        first = :first, 
        second = :second, 
        third = :third, 
        poster = :poster, 
        detail = :detail, 
        update_at = :current_time 
        WHERE id = :id
        """

        args = {
            'id':id,
            'first':first,
            'second':second,
            'third':third,
            'poster':poster,
            'detail':detail,
            'current_time':current_time,
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

        query = "DELETE FROM haikuList WHERE id = :id"
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
def select(id:int,haikuText:str,poster:str,detail:str) -> list[main_const.HaikuListRecord]:
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    args = {}
    query = """SELECT * FROM haikuList where 1 = 1 """
    if id > -1:
        query = query + "and id = :id "
        args['id'] = id
    if poster != '':
        query = query + "and poster like :poster "
        args['poster'] = f"%{poster}%"
    if haikuText != '':
        query = query + "and 1 = 1  and ( first like :haikuText or second like :haikuText or third like :haikuText ) "
        args['haikuText'] = f"%{haikuText}%"
    if detail != '':
        query = query + "and 1 = 1 and ( first like :detail or second like :detail or third like :detail or detail like :detail ) "
        args['detail'] = f"%{detail}%"
    # SELECTクエリを実行
    cursor.execute(query, args)
    results = cursor.fetchall()

    # 結果を表示
    records = []
    for row in results:
        rec = main_const.HaikuListRecord(*row)
        records.append(rec)

    # 接続を閉じる
    conn.close()
    return records