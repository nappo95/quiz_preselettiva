import os
import csv


import csv
import mysql.connector

def create_table_if_not_exists(connection, cursor, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        numer_quesito INT NOT NULL,
        domanda TEXT,
        risposta_corretta TEXT,
        risposta_errata_1 TEXT,
        risposta_errata_2 TEXT,
        risposta_errata_3 TEXT,
        used BOOLEAN DEFAULT FALSE,
        PRIMARY KEY (numer_quesito)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()


def insert_csv_to_mysql(csv_file_path, table_name):
    # 1. Connect to MySQL database
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'quesiti',
        'port': 3306  # Adjust port if needed
    }
    
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        create_table_if_not_exists(connection, cursor, table_name)

        print("Connected to MySQL database successfully.")
        
        # 2. Prepare INSERT statement
        insert_query = f"""
            INSERT INTO {table_name} (numer_quesito, domanda, risposta_corretta, risposta_errata_1, risposta_errata_2,risposta_errata_3)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # 3. Open and read the CSV file
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            
            # If the CSV file has a header, skip it
            next(csvreader, None)  # Comment out if there is no header
            
            # 4. Iterate through CSV rows and insert into the database
            for row in csvreader:
                # row is a list of column values in order [first_name, last_name, email, age, country]
                cursor.execute(insert_query, [element.replace('\n', ' ') for element in row])
            
        # 5. Commit the transaction
        connection.commit()
        print("Data inserted successfully.")
        
    except mysql.connector.Error as error:
        print(f"Error inserting data into MySQL table: {error}")
        
    finally:
        # 6. Close cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

# Usage example
if __name__ == "__main__":
    quesiti_csv = {
        "diritto_commerciale" : "provisioning/quesiti/quesiti_diritto_commerciale.csv",
        "diritto_civile" : "provisioning/quesiti/quesiti_dirtto_civile.csv",
        "diritto_procedura_civile" : "provisioning/quesiti/quesiti_DPC.csv",
        "diritto_tributario" : "provisioning/quesiti/quesitid_diritto_tributario.csv"
    }
    for item in quesiti_csv:
        insert_csv_to_mysql(quesiti_csv[item], item)  # Replace with your table name