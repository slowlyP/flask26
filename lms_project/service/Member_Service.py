from common.db import get_connection




# 로그인
def login(uid, upw):

    conn = get_connection()

    try:
        cur = conn.cursor()

        sql = """
            SELECT * 
            FROM members
            WHERE uid=%s
            AND upw=%s
            AND status='active'
            """

        cur.execute(sql,(uid,upw))
        user = cur.fetchone()

        return user

    finally:
        conn.close()

# 회원가입
def signup(uid, upw, name):

    conn = get_connection()
    
    try:
        cur = conn.cursor()

        sql = """
            INSERT INTO members(uid, upw, name)
            VALUES(%s,%s,%s)
            """

        cur.execute(sql, (uid,upw,name))
        conn.commit()

    finally:
        conn.close()


# mypage

def get_member(uid):
    
    conn = get_connection()

    try:
        cur = conn.cursor()

        sql = """
            SELECT *
            FROM members
            WHERE uid=%s
            """
        cur.execute(sql,( uid,))
        member = cur.fetchone()

        return member
    finally:
        conn.close()


# 회원 정보 update

def update_member(uid, upw, name):

    conn = get_connection()

    try:
        cur = conn.cursor()

        sql = """
            UPDATE members
            SET upw=%s,
                name=%s
            WHERE uid=%s
            """

        cur.execute(sql, (upw, name, uid))
        conn.commit()

    finally:
        conn.close()

# 프로필 사진

def update_profile(uid, filename):

    conn = get_connection()

    try:
        cur = conn.cursor()

        sql = """
            UPDATE members
            SET profile_img=%s
            WHERE uid=%s
            """

        cur.execute(sql, (filename, uid))
        conn.commit()

    finally:
        conn.close()





























# 회원 전체 조회 (관리자 전용)

def get_member_list():
    conn = get_connection()

    try:
        cur = conn.cursor()

        sql = """
            SELECT id, uid, name, role, status, reg_date
            FROM members
            ORDER BY id DESC
            """
        
        cur.execute(sql)
        members= cur.fetchall()

        return members

    finally:
        conn.close()


# 회원 active
def change_status(member_id, status):

    conn = get_connection()

    try:
        cur = conn.cursor()

        sql = """
            UPDATE members
            SET status=%s
            WHERE id=%s
            """
        
        cur.execute(sql, (status, member_id))
        conn.commit()

    finally:
        conn.close()

# 회원 delte
def delete_member(member_id):

    conn = get_connection()

    try:
        cur = conn.cursor()

        sql = """
            DELETE FROM members
            WHERE id=%s
            """

        cur.execute(sql, (member_id,))
        conn.commit()

    finally:
        conn.close()
