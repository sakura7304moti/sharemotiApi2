import sqlite3
from . import scraper_const

database = scraper_const.Database()
dbname = database.twitter_path()


def init():
    """
    CREATE DB,TABLE
    """
    conn = sqlite3.connect(dbname)

    # データベースへのコネクションを閉じる。(必須)
    conn.close()

    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # personsというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute(
        """CREATE TABLE IF NOT EXISTS twitter(
                hashtag STRING,
                mode STRING,
                url STRING,
                date STRING,
                images STRING,
                userId INTEGER,
                userName STRING,
                likeCount INTEGER
                )
                """)

    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()


def _searchQuery(
        page_no:int=1,
        page_size:int=30,
        hashtag:str='',
        start_date:str='',
        end_date:str='',
        user_name:str='',
        mode:str='',
        min_like:int=0,
        max_like:int=0
):
    """
    検索に使用する。クエリとargsを取得。
    """
    #ページング設定
    offset = (max(page_no - 1,0))*page_size  

    query = "SELECT * FROM twitter where 1 = 1 "
    if hashtag != '':
        query = query + "and hashtag like :hashtag "
    if start_date != '' and end_date != '':
        query = query + "and date BETWEEN :start_date AND :end_date "
    if user_name != '':
        query = query + "and userId = :user_name "
    if mode != '':
        query = query + "and mode = :mode "
    if min_like != 0:
        query = query + "and likeCount >= :min_like "
    if max_like != 0:
        query = query + "and :max_like >= likeCount "
    query = query + 'order by date desc,url '
    if page_size != 0:
        limit_sql = 'limit :page_size offset :offset'
        query = query + limit_sql
        
    args = {
        'hashtag':f'%{hashtag}%',
        'start_date':start_date,
        'end_date':end_date,
        'user_name':user_name,
        'mode':mode,
        'min_like':min_like,
        'max_like':max_like,
        'page_size':page_size,
        'offset':offset
    }
    return query,args

def search(
        page_no:int=1,
        page_size:int=30,
        hashtag:str='',
        start_date:str='',
        end_date:str='',
        user_name:str='',
        mode:str='',
        min_like:int=0,
        max_like:int=0
) -> list[scraper_const.TwitterQueryRecord]:
    """
    レコードを取得する
    """
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    # SELECTクエリを実行
    query,args = _searchQuery(
        page_no,
        page_size,
        hashtag,
        start_date,
        end_date,
        user_name,
        mode,
        min_like,
        max_like
    )
    cursor.execute(query,args)
    results = cursor.fetchall()

    # 結果を表示
    records = []
    for row in results:
        rec = scraper_const.TwitterQueryRecord(*row)
        records.append(rec)

    # 接続を閉じる
    conn.close()
    return records


def search_count(
        hashtag:str='',
        start_date:str='',
        end_date:str='',
        user_name:str='',
        mode:str='',
        min_like:int=0,
        max_like:int=0
):
    """
    ページ数を取得する
    """
    query,args = _searchQuery(
        1,
        0,
        hashtag,
        start_date,
        end_date,
        user_name,
        mode,
        min_like,
        max_like)
    
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    #件数のみ取得
    count_query = f'select count(*) from ({query})'
    cursor.execute(count_query,args)
    results = cursor.fetchall()

    return results[0][0]