import sqlite3
from datetime import datetime

DB_PATH = "garden.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_all_plants():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT plant_id, plant_name, species, latest_image FROM plants")
    plants = c.fetchall()
    conn.close()
    return plants

def add_plant(name, image_path, species):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO plants (plant_name, species, latest_image) VALUES (?, ?, ?)",
              (name, species, image_path))
    conn.commit()
    conn.close()

def delete_plant(plant_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM logs WHERE plant_id=?", (plant_id,))
    c.execute("DELETE FROM plants WHERE plant_id=?", (plant_id,))
    conn.commit()
    conn.close()

def get_logs(plant_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT timestamp, disease, cause, solution
        FROM logs
        WHERE plant_id = ?
        ORDER BY timestamp DESC
    """, (plant_id,))
    logs = c.fetchall()
    conn.close()
    return logs

def add_log(plant_id, disease, cause, solution):
    conn = get_connection()
    c = conn.cursor()
    ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    c.execute("""
        INSERT INTO logs (timestamp, plant_id, disease, cause, solution)
        VALUES (?, ?, ?, ?, ?)
    """, (ts, plant_id, disease, cause, solution))
    conn.commit()
    conn.close()

def update_latest_image(plant_id, image_path):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE plants SET latest_image = ? WHERE plant_id = ?", (image_path, plant_id))
    conn.commit()
    conn.close()

def delete_log(timestamp): # timestamp is unique identifier
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM logs WHERE timestamp=?", (timestamp,))
    conn.commit()
    conn.close()
