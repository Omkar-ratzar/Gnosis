import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
        cursor_factory=RealDictCursor
    )
