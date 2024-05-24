import sqlite3
import re
from . import scraper_const

database = scraper_const.Database()
dbname = database.hololewd_path()

def make_table():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS hololewd(
                flair_text STRING,
                url STRING,
                date STRING,
                score INTEGER
                )
                """
    )

    conn.commit()
    conn.close()

#追加
def insert_hololewd(
    flair_text:str,
    url:str,
    date:str,
    score:int
):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = """
    INSERT INTO hololewd 
    SELECT * FROM 
    ( 
        SELECT 
            :flair_text, :url, :date, :score
        WHERE NOT EXISTS
            (SELECT 1 FROM hololewd WHERE flair_text = :flair_text AND url = :url)
    )
    """

    args = {
        "flair_text" : flair_text,
        "url" : url,
        "date" : date,
        "score" : score
    }

    cursor.execute(query, args)
    
    conn.commit()
    conn.close()

def select_hololewd(query:str):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute(query)

    results = cursor.fetchall()
    records = [scraper_const.HololewdQueryRecord(*r) for r in results]
    cursor.close()
    return records

def search(
        page_no:int=1,
        page_size:int=30,
        flair_text:str='',
        min_score:int=100
) -> list[scraper_const.HololewdQueryRecord]:
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    # レコード取得
    query =  "SELECT * FROM hololewd where 1 = 1 and flair_text != 'Yagoo' "
    if flair_text != '':
        query = f"{query} and flair_text like :flair_text "
    if min_score > 0:
        query = f"{query} and score >= :min_score "
    query = f"{query} order by date desc,flair_text,url "
    if page_size != 0:
        sql_query = f"{query} limit :page_size offset :offset"

    args = {
        'flair_text' : f"%{flair_text}%",
        'min_score' : min_score,
        'page_size' : page_size,
        'offset' : max(page_no - 1,0)*page_size
    }

    cursor.execute(sql_query,args)
    results = cursor.fetchall()

    records = []
    for row in results:
        rec = scraper_const.HololewdQueryRecord(*row)
        records.append(rec)

    # 件数取得
    count_query = f'select count(*) from ({query})'
    cursor.execute(count_query,args)
    results = cursor.fetchall()
    search_count = results[0][0]

    conn.close()
    return records , search_count