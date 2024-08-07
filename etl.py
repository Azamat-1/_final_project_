import psycopg2
import pandas as pd

def get_data():
    try:
        # Подключение к базе данных PostgreSQL
        conn = psycopg2.connect(
            dbname='zypl_project', 
            user='postgres', 
            password='yourpassword', 
            host='127.0.0.1', 
            port='5432'
        )
        
        # Выполнение SQL-запроса для извлечения данных
        query = "SELECT * FROM full_customers"
        df = pd.read_sql_query(query, conn)
        
        # Закрытие подключения
        conn.close()
        
        # Вывод всех столбцов в консоль
        print("Columns in the DataFrame:", df.columns.tolist())
        
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame() 