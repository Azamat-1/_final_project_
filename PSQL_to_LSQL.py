import psycopg2
import sqlite3

def fetch_data_from_postgres(postgres_conn_params):
    conn = psycopg2.connect(**postgres_conn_params)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    conn.close()
    return data, column_names

def create_sqlite_db(sqlite_db_path, data, column_names):
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    columns_str = ", ".join(f"{col} TEXT" for col in column_names)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS customers ({columns_str})")

    placeholders = ", ".join("?" for _ in column_names)
    cursor.executemany(f"INSERT INTO customers VALUES ({placeholders})", data)
    conn.commit()
    conn.close()

postgres_conn_params = {
    'dbname': 'zypl_project', 
    'user': 'postgres', 
    'password': 'yourpassword', 
    'host': '127.0.0.1', 
    'port': '5432'
}

sqlite_db_path = 'my.db'

data, column_names = fetch_data_from_postgres(postgres_conn_params)
create_sqlite_db(sqlite_db_path, data, column_names)

print(f"Data has been transferred to {sqlite_db_path}")
