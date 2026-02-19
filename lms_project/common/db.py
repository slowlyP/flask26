import pymysql
from config import *

def get_connection():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

    return conn


if __name__ =="__main__":

    conn = get_connection()
    print("DB 연결 성공")

    conn.close()
