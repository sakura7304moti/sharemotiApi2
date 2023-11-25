"""
焼き直し条約 API
"""
from . import main_const
import sqlite3

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

    # yakiListというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute(
        """CREATE TABLE IF NOT EXISTS yakiList(
                word STRING,
                yaki STRING
                )
                """
    )

    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()


"""
INSERT and UPDATE
"""


def save(word: str = "", yaki: str = ""):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    if word != "":
        # レコードの存在をチェックするためのクエリを作成する
        check_query = "SELECT * FROM yakiList WHERE word = :word"
        cursor.execute(check_query, {"word": word})
        result = cursor.fetchall()

        if not result:
            # 存在しないレコードなら追加する
            query = "INSERT INTO yakiList (word, yaki) VALUES (:word, :yaki)"
            args = {"word": word, "yaki": yaki}
            cursor.execute(query, args)
        else:
            # 存在するレコードなら更新する
            query = "UPDATE yakiList SET yaki = :yaki WHERE word = :word"
            args = {"word": word, "yaki": yaki}
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


def delete(word: str = "", yaki: str = ""):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    # レコードの存在をチェックするためのクエリを作成する
    check_query = f"SELECT * FROM yakiList WHERE word = '{word}'"
    # クエリを実行して結果を取得する
    cursor.execute(check_query)
    result = cursor.fetchall()

    # 存在するレコードなら削除する
    if result != []:
        query = "DELETE FROM yakiList WHERE word = :word and yaki = :yaki"
        args = {"word": word, "yaki": yaki}
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
    query = "SELECT * FROM yakiList WHERE word like :text or yaki like :text"

    args = {"text": f"%{text}%"}
    print("query", query)

    # SELECTクエリを実行
    cursor.execute(query, args)
    results = cursor.fetchall()

    # 結果を表示
    records = []
    for row in results:
        rec = main_const.YakiListRecord(*row)
        records.append(rec)

    # 接続を閉じる
    conn.close()
    return records
