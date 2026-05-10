import sqlite3
from pathlib import Path

DB_PATH = Path("storage/app.db")


def get_db_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    
    cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )            
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_cache (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_hash TEXT NOT NULL,
            keywords     TEXT NOT NULL,
            source       TEXT NOT NULL,      -- 'linkedin' | 'naukri'
            jobs_json    TEXT NOT NULL,
            cached_at    TIMESTAMP NOT NULL,
            expires_at   TIMESTAMP NOT NULL
        )
    """)

    conn.commit()
    conn.close()