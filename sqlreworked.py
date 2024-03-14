import os
import psycopg2

path = os.getcwd()

connection = psycopg2.connect(
    dbname="dbname",
    user="user",
    password="password",
    host="localhost", #default
    port="5432" #default
)

cursor = connection.cursor()

def create_tables():
    csv_files = [f for f in os.listdir(path) if f.endswith(".csv") and not f.startswith("direct_solar_radiation")]
    if not csv_files:
        print("No CSV files found in the specified location.")
        return
    for csv_file in csv_files:
        try:
            full_file = os.path.join(path, csv_file)
            
            table_name = os.path.splitext(csv_file)[0]  # Get table name from file name without extension

            create_command = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            date DATE,
            observation_station VARCHAR,
            average_temperature FLOAT,
            snow_depth FLOAT,
            cloud_coverage FLOAT,
            solar_radiation FLOAT
            );
            """

            copy_command = f"""
            COPY {table_name}(date, observation_station, average_temperature, snow_depth, cloud_coverage, solar_radiation)
            FROM '{full_file}'
            DELIMITER ','
            CSV HEADER
            ENCODING 'UTF-8';
            """

            cursor.execute(create_command)
            cursor.execute(copy_command)
            connection.commit()
            
            print(f"Table {table_name} created and data copied successfully.")
        except Exception as e:
            print(f"Error processing file {csv_file}: {e}")
            connection.rollback()
            continue

def drop_tables():
    csv_files = [f for f in os.listdir(path) if f.endswith(".csv") and not f.startswith("direct_solar_radiation")]
    if not csv_files:
        print("No CSV files found in the specified location.")
        return
    for csv_file in csv_files:
        try:
            table_name = os.path.splitext(csv_file)[0]
            drop_command = f"""
                DROP TABLE IF EXISTS {table_name} CASCADE;
            """
            cursor.execute(drop_command)
            connection.commit()
            print(f"Table {table_name} dropped successfully.")
        except Exception as e:
            print(f"Error dropping table {table_name}: {e}")
            connection.rollback()
            continue

#create_tables()
#drop_tables()

cursor.close()
connection.close()
