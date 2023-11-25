"""
名言集2 API
"""
from . import main_const
import sqlite3
import datetime

output = main_const.Output()


# sns.dbを作成する
# すでに存在していれば、それにアスセスする。
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

    # wordlistというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute(
        """CREATE TABLE IF NOT EXISTS wordList2(
                word STRING,
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


def save(word: str = "", desc: str = ""):
    # 現在の日時を取得
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    if word != "":
        # レコードの存在をチェックするためのクエリを作成する
        check_query = "SELECT * FROM wordList2 WHERE word = :word"
        cursor.execute(check_query, {"word": word})
        result = cursor.fetchall()

        if not result:
            # 存在しないレコードなら追加する
            query = "INSERT INTO wordList2 (word, desc,create_at,update_at) VALUES (:word, :desc, :current_time, :current_time)"
            args = {"word": word, "desc": desc,"current_time":current_time}
            cursor.execute(query, args)
        else:
            # 存在するレコードなら更新する
            query = "UPDATE wordList2 SET desc = :desc, update_at = :current_time WHERE word = :word"
            args = {"word": word, "desc": desc,"current_time":current_time}
            cursor.execute(query, args)

        # 変更をコミットし、接続を閉じる
        conn.commit()
        conn.close()

        return {
            "insert": not result,
            "update": bool(result),
        }
    else:
        return {"insert": False, "update": False}


"""
DELETE
"""


def delete(word: str = "", desc: str = ""):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    # レコードの存在をチェックするためのクエリを作成する
    check_query = f"SELECT * FROM wordList2 WHERE word = '{word}'"
    # クエリを実行して結果を取得する
    cursor.execute(check_query)
    result = cursor.fetchall()

    # 存在するレコードなら削除する
    if result != []:
        query = "DELETE FROM wordlist2 WHERE word = :word and desc = :desc"
        args = {"word": word, "desc": desc}
        # レコードを削除する
        cursor.execute(query, args)

    # 変更をコミットし、接続を閉じる
    conn.commit()
    conn.close()

    # 削除したらtrue,存在しなかったらfalse
    return True if result != [] else False


"""
SELECT
"""


def search(text: str = ""):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    # クエリー設定
    query = "SELECT * FROM wordList2 WHERE word like :text or desc like :text"

    args = {"text": f"%{text}%"}
    print("query", query)

    # SELECTクエリを実行
    cursor.execute(query, args)
    results = cursor.fetchall()

    # 結果を表示
    records = []
    for row in results:
        rec = main_const.WordList2Record(*row)
        records.append(rec)

    # 接続を閉じる
    conn.close()
    return records
