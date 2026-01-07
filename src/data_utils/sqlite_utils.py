import sqlite3

def init_db():
    conn = sqlite3.connect("data/bike_parking.db")
    cursor = conn.cursor()

    with open("data/schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    cursor.executescript(sql)
    conn.commit()
    conn.close()