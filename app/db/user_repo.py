# app/db/user_repo.py

from app.db.connection import get_connection


def create_user(email: str, password_hash: str):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (%s, %s)
            RETURNING id
            """,
            (email, password_hash)
        )
        user = cur.fetchone()
        conn.commit()
        return user
    finally:
        cur.close()
        conn.close()


def get_user_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()
