import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import psycopg2

# Load environment variables
load_dotenv()

# Database configuration
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Create connection
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

# Create tables and COMMIT the changes
with engine.begin() as conn:  # Auto-commit ensures psycopg2 sees the new tables
    with open('sql/create_table.sql') as file:
        conn.execute(text(file.read()))

print("[✔] Tables created or verified.")

# Load dataset
df = pd.read_csv('dataset/cleaned_sales_dataset.csv')
print(f"[✔] Dataset loaded with {df.shape[0]} rows.")

# Insert data using psycopg2 for ON CONFLICT DO NOTHING
conn = engine.raw_connection()
cur = conn.cursor()

# Step 1 - Insert outlets first (respects FK constraint)
outlet_insert = """
    INSERT INTO outlets (outlet_id, establishment_year, outlet_size, location_type, outlet_type)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (outlet_id) DO NOTHING;
"""

for _, row in df.iterrows():
    cur.execute(outlet_insert, (
        row['outlet_id'], row['establishment_year'], row['outlet_size'],
        row['location_type'], row['outlet_type']
    ))

print("[✔] Outlets inserted successfully.")

# Step 2 - Insert product data (avoids duplicates)
product_insert = """
    INSERT INTO products_data (
        product_id, weight, fat_content, product_visibility, product_type, mrp, outlet_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (product_id, outlet_id) DO NOTHING;
"""

for _, row in df.iterrows():
    cur.execute(product_insert, (
        row['product_id'], row['weight'], row['fat_content'], row['product_visibility'],
        row['product_type'], row['mrp'], row['outlet_id']
    ))

# Commit and close connection
conn.commit()
cur.close()
conn.close()

print("[✔] Data inserted successfully into PostgreSQL without duplicates.")
