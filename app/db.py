import sqlite3

def init_db():
    conn = sqlite3.connect("garden.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS plants (
            plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_name TEXT NOT NULL,
            species TEXT,
            latest_image TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            timestamp TEXT PRIMARY KEY,
            plant_id INTEGER,
            disease TEXT,
            cause TEXT,
            solution TEXT,
            FOREIGN KEY (plant_id) REFERENCES plants (plant_id)
        )
    """)

    conn.commit()
    conn.close()
