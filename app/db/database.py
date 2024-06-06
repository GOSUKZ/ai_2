import sqlite3
import json

from app.cars_names import popular_brands


def create_connection():
    conn = sqlite3.connect('my_db.db')
    return conn

# Load JSON data from files
with open('app/data/kolesa.json', 'r', encoding='utf-8') as f:
    cars_data = json.load(f)

with open('app/data/krisha.json', 'r', encoding='utf-8') as f:
    apartments_data = json.load(f)

# Define popular brands mapping


# Normalize car name based on popular brands
def normalize_car_name(car_name):
    for brand, variations in popular_brands.items():
        for variation in variations:
            if variation in car_name.lower():
                return brand.lower()
    return car_name.lower()

# Connect to SQLite database (or create it if it doesn't exist)
conn = create_connection()
cursor = conn.cursor()

# Create cars table with normalized_name column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        model TEXT,
        year TEXT,
        city TEXT,
        mileage TEXT,
        price TEXT,
        url TEXT,
        normalized_name TEXT
    )
''')

# Create apartments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS apartments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rooms TEXT,
        square TEXT,
        price TEXT,
        address TEXT,
        district TEXT,
        url TEXT
    )
''')

conn.commit()

# Insert data into cars table with normalized names
for car in cars_data:
    normalized_name = normalize_car_name(car['name'])
    price_with_symbol = f"{car['price']} ₸"
    cursor.execute('''
        INSERT INTO cars (name, model, year, city, mileage, price, url, normalized_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (car['name'], car['model'], car['year'], car['city'], car['mileage'], price_with_symbol, car['url'], normalized_name))

# Insert data into apartments table with price in Tenge
for apartment in apartments_data:
    price_with_symbol = f"{apartment['price']} ₸"
    cursor.execute('''
        INSERT INTO apartments (rooms, square, price, address, district, url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (apartment['rooms'], apartment['square'], price_with_symbol, apartment['address'], apartment['district'], apartment['url']))

conn.commit()
conn.close()
