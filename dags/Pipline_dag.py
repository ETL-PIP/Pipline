from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient
from datetime import datetime, date
import mysql.connector
import json
import os
import sqlite3

# Path to the directory containing JSON files
DATA_DIR = '/opt/airflow/dags/data/'

# MongoDB connection URI
mongo_uri = "mongodb+srv://admin:samir5636@cluster0.ghz8l.mongodb.net/?retryWrites=true&w=majority"

def combine_json_data():
    """Reads and combines data from all JSON files in the data directory with newline-separated JSON objects."""
    combined_data = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, 'r') as file:
                for line in file:
                    data = json.loads(line.strip())
                    combined_data.append(data)
    return combined_data

def store_in_mongodb(**context):
    """Stores only new JSON data in MongoDB Atlas, avoiding duplicates."""
    combined_data = context['ti'].xcom_pull(task_ids='combine_json_data')
    client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
    db = client["sample_mflix"]
    collection = db["data1"]
    
    for document in combined_data:
        if not collection.find_one({"appearance_id": document["appearance_id"]}):
            collection.insert_one(document)

def retrieve_mysql_data():
    """Connects to MySQL, retrieves data from the player_appearances table, and returns it as a list of dictionaries."""
    mysql_data = []
    try:
        conn = mysql.connector.connect(
            host="mysql_container",  # Ensure this matches your Docker setup (use container name if needed)
            user="admin",
            password="modepass",
            database="mydatabase"
        )
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM player_appearances"
        cursor.execute(query)
        mysql_data = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
    return mysql_data

def convert_dates(document):
    """Converts any date objects to datetime in a document."""
    for key, value in document.items():
        if isinstance(value, date) and not isinstance(value, datetime):
            document[key] = datetime(value.year, value.month, value.day)
    return document

def store_mysql_data_in_mongodb(**context):
    """Stores MySQL data in MongoDB Atlas, avoiding duplicates based on 'appearance_id'."""
    mysql_data = context['ti'].xcom_pull(task_ids='retrieve_mysql_data')
    client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
    db = client["sample_mflix"]
    collection = db["data1"]

    for document in mysql_data:
        document = convert_dates(document)
        if not collection.find_one({"appearance_id": document["appearance_id"]}):
            collection.insert_one(document)
        else:
            print(f"Document with appearance_id {document['appearance_id']} already exists.")

def process_sqlite_files():
    """Processes all tables in each SQLite file in the data directory and returns the data as a list of dictionaries."""
    combined_sqlite_data = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.db'):
            sqlite_file_path = os.path.join(DATA_DIR, filename)
            with sqlite3.connect(sqlite_file_path) as conn:
                conn.row_factory = sqlite3.Row  # Enables column access by name
                cursor = conn.cursor()

                # Get all table names in the database
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [table[0] for table in cursor.fetchall()]

                # Process each table
                for table_name in tables:
                    query = f"SELECT * FROM {table_name}"
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    # Convert rows to dictionaries and add to combined data list
                    combined_sqlite_data.extend([dict(row) for row in rows])
                    print(f"Processed {len(rows)} records from table '{table_name}' in {filename}")
    
    return combined_sqlite_data

def store_sqlite_data_in_mongodb(**context):
    """Stores SQLite data in MongoDB Atlas, avoiding duplicates based on 'appearance_id'."""
    data = context['ti'].xcom_pull(task_ids='process_sqlite_files')
    with MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True) as client:
        db = client["sample_mflix"]
        collection = db["data1"]

        new_documents = []
        for document in data:
            # Convert date fields to datetime, if necessary
            document = convert_dates(document)

            # Check if the document contains a valid appearance_id
            appearance_id = document.get("appearance_id")
            if appearance_id:
                # Only add the document if it does not already exist in the collection
                if not collection.find_one({"appearance_id": appearance_id}):
                    new_documents.append(document)
            else:
                # Log a message if appearance_id is missing
                print(f"Skipping document because 'appearance_id' is missing: {document}")

        # Perform a bulk insert of all new documents
        if new_documents:
            collection.insert_many(new_documents)
            print(f"Inserted {len(new_documents)} new documents into MongoDB.")
        else:
            print("No new documents to insert.")

# Define the DAG
with DAG(
    'mongo_pipeline',
    default_args={'retries': 1},
    schedule_interval='@daily',
    start_date=datetime(2024, 11, 7),
    catchup=False,
) as dag:
    
    combine_json_data_task = PythonOperator(
        task_id="combine_json_data",
        python_callable=combine_json_data
    )

    store_data_task = PythonOperator(
        task_id="store_in_mongodb",
        python_callable=store_in_mongodb,
        provide_context=True
    )

    retrieve_mysql_data_task = PythonOperator(
        task_id="retrieve_mysql_data",
        python_callable=retrieve_mysql_data
    )

    store_mysql_data_in_mongodb_task = PythonOperator(
        task_id="store_mysql_data_in_mongodb",
        python_callable=store_mysql_data_in_mongodb,
        provide_context=True
    )
    
    process_sqlite_data_task = PythonOperator(
        task_id="process_sqlite_files",
        python_callable=process_sqlite_files
    )

    store_sqlite_data_task = PythonOperator(
        task_id="store_sqlite_data_in_mongodb",
        python_callable=store_sqlite_data_in_mongodb,
        provide_context=True
    )

    # Set task dependencies
    combine_json_data_task >> store_data_task >> retrieve_mysql_data_task >> store_mysql_data_in_mongodb_task >>process_sqlite_data_task >> store_sqlite_data_task
