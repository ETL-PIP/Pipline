from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient
from datetime import datetime
import json
import os

# Path to the directory containing JSON files
DATA_DIR = '/opt/airflow/dags/data/'

def combine_json_data():
    """Reads and combines data from all JSON files in the data directory with newline-separated JSON objects."""
    combined_data = []

    # Iterate over all files in the data directory
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, 'r') as file:
                # Each line is a separate JSON object
                for line in file:
                    data = json.loads(line.strip())  # Parse each line as JSON
                    combined_data.append(data)  # Append dictionary to the list
    
    return combined_data

def store_in_mongodb(**context):
    """Stores only new JSON data in MongoDB Atlas, avoiding duplicates."""
    # Retrieve the combined data from XCom
    combined_data = context['ti'].xcom_pull(task_ids='combine_json_data')
    
    # MongoDB connection URI
    mongo_uri = "mongodb+srv://admin:samir5636@cluster0.ghz8l.mongodb.net/?retryWrites=true&w=majority"
    
    # Connect to MongoDB Atlas
    client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
    db = client["sample_mflix"]  # Set the database name as seen in MongoDB Atlas
    collection = db["combined_data_collection"]  # Set the collection name as seen in MongoDB Atlas
    
    # Insert only new data into MongoDB
    for document in combined_data:
        # Check if the document already exists in the collection
        if not collection.find_one({"appearance_id": document["appearance_id"]}):  # Use 'appearance_id' as unique identifier
            collection.insert_one(document)

# Define the DAG
with DAG(
    'mongo_json_pipeline',
    default_args={'retries': 1},
    schedule_interval='@daily',
    start_date=datetime(2024, 11, 7),
    catchup=False,
) as dag:
    
    # Task 1: Combine JSON data from all files in the data directory
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
