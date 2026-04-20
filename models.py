import sqlite3
from datetime import datetime

DB_NAME = "database.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                url TEXT,
                username_enc TEXT NOT NULL,
                password_enc TEXT NOT NULL,
                notes TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS app_state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        cursor = conn.execute("SELECT * FROM app_state WHERE key='is_initialized'")
        if not cursor.fetchone():
            conn.execute("INSERT INTO app_state (key, value) VALUES ('is_initialized', '0')")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS password_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                credential_id INTEGER,
                password_hash TEXT,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def is_first_run():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("SELECT value FROM app_state WHERE key='is_initialized'")
        return cursor.fetchone()[0] == '0'

def set_initialized():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE app_state SET value='1' WHERE key='is_initialized'")

def save_credential(service, url, username_enc, password_enc, notes, tags):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            "INSERT INTO credentials (service, url, username_enc, password_enc, notes, tags) VALUES (?,?,?,?,?,?)",
            (service, url, username_enc, password_enc, notes, tags)
        )
        return cursor.lastrowid

def get_all_credentials():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM credentials ORDER BY created_at DESC").fetchall()

def get_credential_by_id(cred_id):
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM credentials WHERE id = ?", (cred_id,)).fetchone()

def update_credential(cred_id, service, url, username_enc, password_enc, notes, tags):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE credentials SET service=?, url=?, username_enc=?, password_enc=?, notes=?, tags=? WHERE id=?",
            (service, url, username_enc, password_enc, notes, tags, cred_id)
        )

def delete_credential(cred_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM credentials WHERE id = ?", (cred_id,))

def check_password_reuse(current_password_enc, master_password):
    """Bir xil parol boshqa entrylarda ishlatilganmi tekshirish"""
    from crypto_utils import decrypt_data
    with sqlite3.connect(DB_NAME) as conn:
        all_creds = conn.execute("SELECT id, password_enc FROM credentials").fetchall()
    
    reused = []
    current_password = decrypt_data(current_password_enc, master_password)
    
    for cred_id, enc_password in all_creds:
        try:
            decrypted = decrypt_data(enc_password, master_password)
            if decrypted == current_password:
                reused.append(cred_id)
        except:
            pass
    return reused