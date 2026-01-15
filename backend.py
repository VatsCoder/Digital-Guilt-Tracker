import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect("guilt_tracker.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS guilt_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        emotion TEXT NOT NULL,
        guilt_rate INTEGER NOT NULL,
        reason TEXT NOT NULL,
        control TEXT NOT NULL,
        score INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(name, age, email, password):
    conn = sqlite3.connect("guilt_tracker.db")
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (name, age, email, password) VALUES (?, ?, ?, ?)",
            (name, age, email, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect("guilt_tracker.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, password FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()
    if row and row[2] == hash_password(password):
        return (row[0], row[1])  # (user_id, name)
    return None

def get_last_score(user_id):
    conn = sqlite3.connect("guilt_tracker.db")
    c = conn.cursor()
    c.execute("SELECT score FROM guilt_events WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None  

def save_guilt_entry(user_id,date, emotion, guilt, reason, trigger, score):
    conn = sqlite3.connect("guilt_tracker.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO guilt_events (user_id, date, emotion, guilt_rate, reason, control, score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, date, emotion, guilt, reason, trigger, score))
    conn.commit()
    conn.close()

def get_today_score(user_id, today):
    conn = sqlite3.connect("guilt_tracker.db")
    c = conn.cursor()
    c.execute("""
        SELECT COALESCE(SUM(score), 0)
        FROM guilt_events
        WHERE user_id=? AND date=?
    """, (user_id, today))
    row = c.fetchone()
    return row[0] if row else None

def get_weekly_guilt_entries(user_id, start_date):
    """
    Fetch all guilt entries for the current week starting from start_date.
    Returns a list of tuples: (date, score, id)
    """
    conn = sqlite3.connect("guilt_tracker.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT date, score, id FROM guilt_events
        WHERE user_id=? AND date>=?
        ORDER BY date ASC, id ASC
    """, (user_id, start_date))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_all_logs(user_id):
    conn = sqlite3.connect("guilt_tracker.db")
    c=conn.cursor()
    c.execute("SELECT date,emotion,reason,guilt_rate, score FROM guilt_events WHERE user_id=? ORDER BY date DESC",(user_id,))
    return c.fetchall()

def delete_log(user_id, date, emotion, guilt_rate, control, score):
    conn = sqlite3.connect("guilt_tracker.db")
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM guilt_events
        WHERE user_id=? AND date=? AND emotion=? AND guilt_rate=? AND control=? AND score=?
        """, (user_id, date, emotion, guilt_rate, control, score))
    conn.commit()
    conn.close()

