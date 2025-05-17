import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Таблица товаров на складе
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            variations TEXT,
            purchase_price REAL,
            delivery_cost REAL,
            with_delivery INTEGER,
            total_cost REAL,
            date TEXT,
            history TEXT
        )
    ''')

    # Таблица продаж
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            color TEXT,
            size TEXT,
            quantity INTEGER,
            sell_price REAL,
            platform TEXT,
            date TEXT,
            comment TEXT
        )
    ''')

    # Таблица расходов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            amount REAL,
            date TEXT,
            comment TEXT
        )
    ''')

    # Таблица заметок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()
