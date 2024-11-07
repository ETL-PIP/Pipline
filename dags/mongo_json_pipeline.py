from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient
from datetime import datetime
import json
import os

# Paths to the JSON files
FILE1_PATH = '/opt/airflow/dags/data/file1.json'
FILE2_PATH = '/opt/airflow/dags/data/file2.json'

def combine_json_data():
    """Reads and combines data from two JSON files."""
    with open(FILE1_PATH) as file1, open(FILE2_PATH) as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)
        
        # Combine data based on structure (lists or dictionaries)
        if isinstance(data1, list) and isinstance(data2, list):
            combined_data = data1 + data2  # Concatenate lists
        else:
            combined_data = {**data1, **data2}  # Merge dictionaries
        
        return combined_data

def store_in_mongodb(**context):
    """Stores combined JSON data in MongoDB Atlas."""
    # Retrieve the combined data from XCom
    combined_data = context['ti'].xcom_pull(task_ids='combine_json_data')
    
    # Direct MongoDB connection URI (replace BaseHook with direct URI for troubleshooting)
    mongo_uri = "mongodb+srv://admin:samir5636@cluster0.ghz8l.mongodb.net/?retryWrites=true&w=majority"
    
    # Connect to MongoDB Atlas
    client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
    db = client["sample_mflix"]  # Set the database name as seen in MongoDB Atlas
    collection = db["combined_data_collection"]  # Set the collection name as seen in MongoDB Atlas
    
    # Insert combined data into MongoDB
    if isinstance(combined_data, list):
        collection.insert_many(combined_data)  # Insert list of documents
    else:
        collection.insert_one(combined_data)  # Insert single document if not a list

# Define the DAG
with DAG(
    'mongo_json_pipeline',
    default_args={'retries': 1},
    schedule_interval='@daily',
    start_date=datetime(2024, 11, 7),
    catchup=False,
) as dag:
    
    # Task 1: Combine JSON data from two files
    combine_json_data_task = PythonOperator(
        task_id="combine_json_data",
        python_callable=combine_json_data
    )

    # Task 2: Store the combined data in MongoDB Atlas
    store_data_task = PythonOperator(
        task_id="store_in_mongodb",
        python_callable=store_in_mongodb,
        provide_context=True
    )

    # Set task dependencies
    combine_json_data_task >> store_data_task
