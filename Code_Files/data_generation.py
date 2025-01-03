import csv
import random
import string
import os
import datetime
import time

# Variables
DIRTY_DATA_PROBABILITY = 0.1  # Probability of introducing dirty data

# Paths for CSVs
CUSTOMER_FILE = "customers.csv"
PRODUCT_FILE = "products.csv"
ORDER_FILE = "orders.csv"

# Sample data pools
FIRST_NAMES = ["John", "Jane", "Emily", "Michael", "Chris", "Sarah", "David", "Anna", "James", "Laura"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Martinez", "Hernandez"]
CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
EMAIL_DOMAINS = ["@gmail.com", "@yahoo.com", "@icloud.com", "@hotmail.com", "@outlook.com"]
PRODUCTS = [
    ("Ultraboost 22", "Shoes"),
    ("Adilette Slides", "Shoes"),
    ("Trefoil Hoodie", "Clothing"),
    ("4D Fusio", "Shoes"),
    ("Forum Low Shoes", "Shoes"),
    ("AEROREADY Backpack", "Accessories"),
    ("Primeblue Shorts", "Clothing"),
    ("ZX 2K Boost Shoes", "Shoes"),
    ("Alphaskin Tights", "Clothing"),
    ("R.Y.V. Crossbody Bag", "Accessories")
]

# Estimate average row size in bytes
AVERAGE_CUSTOMER_ROW_SIZE = 100
AVERAGE_ORDER_ROW_SIZE = 150

# Generate random data functions
def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_email(first_name, last_name):
    domain = random.choice(EMAIL_DOMAINS)
    return f"{first_name.lower()}.{last_name.lower()}{domain}"

def random_phone():
    return int(''.join(random.choices(string.digits, k=10)))

def random_date(start_year=2015, end_year=2023):
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + datetime.timedelta(days=random_days)

# Data generation
customers = []
products = []
orders = []

# Generate Customers
def generate_customers(num_customers):
    for i in range(1, num_customers + 1):
        customer_id = i
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}" if random.random() > DIRTY_DATA_PROBABILITY else None
        email = random_email(first_name, last_name) if random.random() > DIRTY_DATA_PROBABILITY else "invalid_email"
        phone = random_phone() if random.random() > DIRTY_DATA_PROBABILITY else None
        age = random.randint(18, 80) if random.random() > DIRTY_DATA_PROBABILITY else -1
        gender = random.choice(['M', 'F', 'O', None])
        location = random.choice(CITIES) if random.random() > DIRTY_DATA_PROBABILITY else ""
        customers.append([customer_id, name, email, phone, age, gender, location])

def generate_products():
    for i, (product_name, category) in enumerate(PRODUCTS, start=1):
        product_id = i
        price = random.randint(50, 300) if random.random() > DIRTY_DATA_PROBABILITY else -1
        stock_quantity = random.randint(0, 1000) if random.random() > DIRTY_DATA_PROBABILITY else -1
        products.append([product_id, product_name, category, price, stock_quantity])

def generate_orders(num_orders):
    for i in range(1, num_orders + 1):
        order_id = i
        customer_id = random.randint(1, len(customers))
        product_id = random.randint(1, len(products))
        quantity = random.randint(1, 10) if random.random() > DIRTY_DATA_PROBABILITY else -1
        total_amount = random.randint(50, 3000) if random.random() > DIRTY_DATA_PROBABILITY else -1
        transaction_date = random_date()
        payment_method = random.choice(["Credit Card", "Debit Card", "PayPal", "Cash", None])
        orders.append([order_id, customer_id, product_id, quantity, total_amount, transaction_date, payment_method])

# Write data to CSVs
def write_csv(filename, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Main function
def main():
    size_in_gb = float(input("Enter the size of data to generate (in GB): "))
    total_size_in_bytes = size_in_gb * 1024 * 1024 * 1024

    num_customers = int(total_size_in_bytes * 0.2 / AVERAGE_CUSTOMER_ROW_SIZE)  # 60% for customers
    num_orders = int(total_size_in_bytes * 0.8 / AVERAGE_ORDER_ROW_SIZE)  # 40% for orders

    print(f"Generating approximately {num_customers} customers and {num_orders} orders...")

    generate_customers(num_customers)
    generate_products()  # Fixed number of products
    generate_orders(num_orders)

    # Write data to CSV files
    write_csv(CUSTOMER_FILE, customers)
    write_csv(PRODUCT_FILE, products)
    write_csv(ORDER_FILE, orders)
    print("Data generation completed.")

if __name__ == "__main__":
    main()
