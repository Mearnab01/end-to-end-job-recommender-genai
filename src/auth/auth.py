from src.database.db import get_db_connection
from utils.logger import get_logger

logger = get_logger("auth")

def login_or_register(username:str) -> dict:
    """
    If the username exists → log in.
    If it doesn't → register it automatically.
 
    Returns a plain dict: { id, username, created_at, is_new }
    """
    username = username.strip().lower()
 
    conn = get_db_connection()
    cur  = conn.cursor()
    
    cur.execute(
        "SELECT id, username, created_at FROM users WHERE username = ?",
        (username,),
    )
    row = cur.fetchone()
    
    if row:
        logger.info("User login | username=%s", username)
        conn.close()
        return {
            "id":         row["id"],
            "username":   row["username"],
            "created_at": row["created_at"],
            "is_new":     False,
        }
        
    # New user — insert
    cur.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    
    logger.info("New user registered | username=%s | id=%s", username, new_id)
    return {
        "id":         new_id,
        "username":   username,
        "created_at": None,
        "is_new":     True,
    }
