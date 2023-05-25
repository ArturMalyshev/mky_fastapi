import hashlib
import time


def create_session(db):
    uniq_string = bytearray(str(time.time()), 'utf-8')
    new_session_key = hashlib.sha256(uniq_string).hexdigest()

    sql = "INSERT INTO sessions (session_key, created_at, updated_at)  VALUES (%s, NOW(), NOW())"
    cursor = db.cursor()
    cursor.execute(sql, [new_session_key])
    db.commit()
    return new_session_key


def get_session_id(db, session_key):
    sql = "SELECT session_id FROM sessions WHERE session_key=%s;"
    db.execute(sql, [session_key])
    for session in db:
        return session[0]


def update_session_date(db, session_key):
    updater = db.cursor()
    sql = "UPDATE sessions SET updated_at=NOW() WHERE session_key=%s"
    updater.execute(sql, [session_key])
    db.commit()




