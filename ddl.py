import psycopg2

def execute_ddl():
    try:
        conn = psycopg2.connect(
            dbname='zypl_project', 
            user='postgres', 
            password='yourpassword', 
            host='127.0.0.1', 
            port='5432'
        )
        cur = conn.cursor()
        
        ddl_script = """
        DROP TABLE IF EXISTS full_customers;

        CREATE TABLE full_customers (
            ID VARCHAR(255),
            Customer_ID VARCHAR(255),
            Month VARCHAR(50),
            Name VARCHAR(255),
            Age INT,
            SSN VARCHAR(255),
            Occupation VARCHAR(255),
            Annual_Income FLOAT,
            Monthly_Inhand_Salary FLOAT,
            Num_Bank_Accounts INT,
            Num_Credit_Card INT,
            Interest_Rate INT,
            Num_of_Loan INT,
            Type_of_Loan TEXT,
            Delay_from_due_date INT,
            Num_of_Delayed_Payment INT,
            Changed_Credit_Limit FLOAT,
            Num_Credit_Inquiries INT,
            Credit_Mix VARCHAR(50),
            Outstanding_Debt FLOAT,
            Credit_Utilization_Ratio FLOAT,
            Credit_History_Age VARCHAR(255),
            Payment_of_Min_Amount VARCHAR(255),
            Total_EMI_per_month FLOAT,
            Amount_invested_monthly FLOAT,
            Payment_Behaviour VARCHAR(255),
            Monthly_Balance FLOAT
        );
        """
        
        cur.execute(ddl_script)
        conn.commit()
        cur.close()
        conn.close()
        print("DDL script executed successfully.")
    except Exception as e:
        print(f"Error: {e}")

execute_ddl()
