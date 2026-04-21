from app.db.file_repo import get_file_id_by_path
from psycopg2.extras import RealDictCursor
from app.db.connection import get_connection


conn = get_connection()
cursor = conn.cursor()
path=input("Enter the path to which u wanna try file id for")
print(get_file_id_by_path(path))
# cursor.execute("SELECT file_path FROM all_files WHERE file_id = 5135;")
# cursor.execute("SELECT file_id FROM all_files WHERE file_path = '/opt/airflow/app/data/tree.jpg'")
# print(cursor.fetchone())
