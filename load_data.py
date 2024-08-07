import pandas as pd
from sqlalchemy import create_engine

def load_data():
    # Путь к вашему CSV файлу
    csv_file_path = '/Users/bad_boy/Zypl final project/new_try/data/processed_test.csv'
    
    # Создание соединения с использованием SQLAlchemy
    engine = create_engine('postgresql://postgres:yourpassword@127.0.0.1:5432/zypl_project')
    
    # Загрузка данных из CSV файла в DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Загрузка данных из DataFrame в таблицу full_customers
    df.to_sql('full_customers', engine, if_exists='replace', index=False)
    
    print("Data loaded successfully.")

load_data()