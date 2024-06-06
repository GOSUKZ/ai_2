import json
from app.db.database import create_connection, popular_brands


def normalize_car_name(car_name):
    for brand, variations in popular_brands.items():
        for variation in variations:
            if variation in car_name.lower():
                return brand.lower()
    return car_name.lower()
def find_cars_by_price(price):
    conn = create_connection()
    cursor = conn.cursor()
    min_price = price * 0.8
    max_price = price * 1.2
    cursor.execute("SELECT name, model, year, price, url FROM cars WHERE price BETWEEN ? AND ? LIMIT 10",
                   (min_price, max_price))
    cars = cursor.fetchall()
    conn.close()
    if cars:
        return json.dumps({"cars": cars})
    else:
        return json.dumps({"error": "No cars found in the specified price range."})


def find_cars_by_name(name):
    conn = create_connection()
    cursor = conn.cursor()

    # Normalize the input name
    normalized_name = normalize_car_name(name)

    # Search in the normalized_name column
    cursor.execute("SELECT name, model, year, price, url FROM cars WHERE normalized_name = ? LIMIT 10",
                   (normalized_name,))
    cars = cursor.fetchall()
    conn.close()

    if cars:
        return json.dumps({"cars": cars})
    else:
        return json.dumps({"error": "No cars found with the specified name."})


def find_cars_by_model(model):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, model, year, price, url FROM cars WHERE model = ? LIMIT 10", (model,))
    cars = cursor.fetchall()
    conn.close()
    if cars:
        return json.dumps({"cars": cars})
    else:
        return json.dumps({"error": "No cars found with the specified model."})


def find_cars_by_mileage(mileage):
    conn = create_connection()
    cursor = conn.cursor()
    max_mileage = mileage * 1.2
    cursor.execute("SELECT name, model, year, price, url FROM cars WHERE mileage <= ? LIMIT 10", (mileage))
    cars = cursor.fetchall()
    conn.close()
    if cars:
        return json.dumps({"cars": cars})
    else:
        return json.dumps({"error": "No cars found with the specified mileage."})


def find_cars_by_year(year):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, model, year, price, url FROM cars WHERE year = ? LIMIT 10", (year,))
    cars = cursor.fetchall()
    conn.close()
    if cars:
        return json.dumps({"cars": cars})
    else:
        return json.dumps({"error": "No cars found with the specified year."})


def find_apartments_by_square(square):
    conn = create_connection()
    cursor = conn.cursor()
    min_square = square * 0.8
    max_square = square * 1.2
    cursor.execute(
        "SELECT rooms, square, price, address, district, url FROM apartments WHERE square BETWEEN ? AND ? LIMIT 10",
        (min_square, max_square))
    apartments = cursor.fetchall()
    conn.close()
    if apartments:
        return json.dumps({"apartments": apartments})
    else:
        return json.dumps({"error": "No apartments found in the specified square footage range."})


def find_apartments_by_address(address):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rooms, square, price, address, district, url FROM apartments WHERE address = ? LIMIT 10",
                   (address,))
    apartments = cursor.fetchall()
    conn.close()
    if apartments:
        return json.dumps({"apartments": apartments})
    else:
        return json.dumps({"error": "No apartments found with the specified address."})


def find_apartments_by_price(price):
    conn = create_connection()
    cursor = conn.cursor()
    min_price = price * 0.8
    max_price = price * 1.2
    cursor.execute(
        "SELECT rooms, square, price, address, district, url FROM apartments WHERE price BETWEEN ? AND ? LIMIT 10",
        (min_price, max_price))
    apartments = cursor.fetchall()
    conn.close()
    if apartments:
        return json.dumps({"apartments": apartments})
    else:
        return json.dumps({"error": "No apartments found in the specified price range."})


import json
from app.db.database import create_connection

def find_apartments_by_district(district):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rooms, square, price, address, district, url FROM apartments WHERE LOWER(district) = LOWER(?) LIMIT 10", (district,))
    apartments = cursor.fetchall()
    conn.close()
    if apartments:
        return json.dumps({"apartments": apartments})
    else:
        return json.dumps({"error": "No apartments found in the specified district."})
