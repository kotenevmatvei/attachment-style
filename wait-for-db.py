import sys
import time
import os
import psycopg2
from psycopg2 import OperationalError

print("Waiting for database...")

retries = 20
while retries > 0:
    try:
        db_url = os.environ['DB_URL']
        conn = psycopg2.connect(db_url)
        conn.close()
        print("Database is ready!")
        sys.exit(0) 
    except OperationalError:
        retries -= 1
        print(f"Database not ready, retrying... ({retries} retries left)")
        time.sleep(1)

print("Error: Could not connect to database after several retries.")
sys.exit(1) 

