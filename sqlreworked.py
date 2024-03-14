import os
import psycopg2

path = os.getcwd()
csvfolderslocation = path + "\\data\\"

connection = psycopg2.connect(
    dbname="your_database",
    user="your_user",
    password="your_password",
    host="localhost", #default
    port="5432" #default
)

cursor = connection.cursor()

def create_tables():
    csvfolders = [f for f in os.listdir(csvfolderslocation) if os.path.isdir(os.path.join(csvfolderslocation, f))]
    csvfolders = [f for f in csvfolders if not f.startswith('.')]
    for i in csvfolders:
        directory = os.path.join(csvfolderslocation, i)
        try:
            full_file = next(file for file in os.listdir(directory) if file.endswith(f"{i}.csv"))
        except StopIteration:
            print(f"No {i}.csv file found in {i}")
            continue

        create_command = f"""
        CREATE TABLE IF NOT EXISTS {i} (
        id SERIAL PRIMARY KEY,
        observation_station VARCHAR,
        date DATE,
        snow_depth FLOAT,
        average_temperature FLOAT,
        cloud_coverage FLOAT,
        solar_radiation FLOAT
        );
        """

        copy_command = f"""
        COPY {i}(observation_station, date, snow_depth, average_temperature, cloud_coverage, solar_radiation)
        FROM '{os.path.join(directory, full_file)}'
        DELIMITER ','
        CSV HEADER
        ENCODING 'UTF-8';
        """

        try:
            cursor.execute(create_command)
        except psycopg2.Error as e:
            print(f"Error creating table for {i}: {e}")
            continue
    
        try:
            cursor.execute(copy_command, (os.path.join(directory, full_file),))
            connection.commit()
        except psycopg2.Error as e:
            print(f"Error copying data for {i}: {e}")
            connection.rollback()
            continue

def drop_tables():
    csvfolders = [f for f in os.listdir(csvfolderslocation) if os.path.isdir(os.path.join(csvfolderslocation, f))]
    csvfolders = [f for f in csvfolders if not f.startswith('.')]
    for i in csvfolders:
        drop_command = f"""
            DROP TABLE IF EXISTS {i} CASCADE;
        """
        cursor.execute(drop_command)
        connection.commit()

create_tables()

cursor.close()
connection.close()