import sqlite3

DB = "bot.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        plan TEXT,
        last_gen TEXT,
        total_gen INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def create_user(user_id, username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    INSERT OR IGNORE INTO users (user_id, username, plan, last_gen, total_gen)
    VALUES (?, ?, 'Demo', '', 0)
    """, (user_id, username))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()

    conn.close()
    return user


def update_gen(user_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    UPDATE users
    SET last_gen = datetime('now'),
        total_gen = total_gen + 1
    WHERE user_id=?
    """, (user_id,))

    conn.commit()
    conn.close()
