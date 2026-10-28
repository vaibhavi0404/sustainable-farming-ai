import sqlite3
from datetime import datetime

DB_NAME = "farming_data.db"


def create_database():
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS farming_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soil_summary TEXT,
            weather_summary TEXT,
            market_summary TEXT,
            recommendation TEXT,
            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_report(soil, weather, market, recommendation):
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        INSERT INTO farming_reports
        (soil_summary, weather_summary, market_summary,
         recommendation, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        soil,
        weather,
        market,
        recommendation,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_reports():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.execute(
        "SELECT * FROM farming_reports ORDER BY id DESC"
    )
    reports = cursor.fetchall()
    connection.close()
    return reports