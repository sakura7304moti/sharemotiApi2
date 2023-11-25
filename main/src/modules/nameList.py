"""
あだ名一覧 API
"""
from . import main_const
import sqlite3


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

    # keylistというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute(
        """CREATE TABLE IF NOT EXISTS nameList(
                key STRING,
                val STRING
                )
                """
    )

    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()


"""
INSERT and UPDATE
"""


def insert(key: str = "", val: str = ""):
    if key != "" and val != "":
        records = search(key, val)
        if len(records) == 0:
            # データベースに接続する
            conn = sqlite3.connect(dbname)
            cursor = conn.cursor()

            # 存在しないレコードなら追加する
            query = "INSERT INTO nameList (key, val) VALUES (:key, :val)"
            args = {"key": key, "val": val}
            cursor.execute(query, args)

            # データベースへコミット。これで変更が反映される。
            conn.commit()
            conn.close()
        return {
            "insert": len(records) == 0,
            "update": False,
        }
    else:
        return {"insert": False, "update": False}


def check_name_existence(
    name_list: list[main_const.NameListRecord], target_key: str
) -> bool:
    for record in name_list:
        if record.key == target_key:
            return True
    return False


def update(bkey: str = "", bval: str = "", key: str = "", val: str = ""):
    if key != "" and val != "":
        records = search("", val)
        if check_name_existence(records, key) == False:
            # データベースに接続する
            conn = sqlite3.connect(dbname)
            cursor = conn.cursor()

            # 存在するレコードなら更新する
            query = "UPDATE nameList SET key = :key WHERE val = :bval and key = :bkey"
            args = {"bkey": bkey, "bval": bval, "key": key}
            cursor.execute(query, args)

            # 変更をコミットし、接続を閉じる
            conn.commit()
            conn.close()

        return {
            "insert": False,
            "update": check_name_existence(records, key) == False,
        }
    else:
        return {"insert": False, "update": False}


"""
DELETE
"""


def delete(key: str = "", val: str = ""):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    records = search(key, val)

    # 存在するレコードなら削除する
    if len(records) != 0:
        query = "DELETE FROM namelist WHERE key = :key and val = :val"
        args = {"key": key, "val": val}
        # レコードを削除する
        cursor.execute(query, args)

    # 変更をコミットし、接続を閉じる
    conn.commit()
    conn.close()

    # 削除したらtrue,存在しなかったらfalse
    return True if len(records) != 0 else False


"""
SELECT
"""


def search(key: str = "", val: str = ""):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    # クエリー設定
    query = "SELECT * FROM nameList WHERE 1 = 1 "
    if key != "":
        query = query + "and key like :key "
    if val != "":
        query = query + "and val like :val "
    query = query + "order by val,key"

    args = {"key": f"%{key}%", "val": f"%{val}%"}
    print("query", query)

    # SELECTクエリを実行
    cursor.execute(query, args)
    results = cursor.fetchall()

    # 結果を表示
    records = []
    for row in results:
        rec = main_const.NameListRecord(*row)
        records.append(rec)

    # 接続を閉じる
    conn.close()
    return records


def init_update():
    df = main_const.ssbu_dict()
    for index, row in df.iterrows():
        key = row["key"]
        val = row["val"]
        insert(key, val)
