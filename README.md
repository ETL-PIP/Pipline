# Pipline
building a data pipeline with Apache Airflow to load data from multiple sources into a data warehouse 
![architecture](https://github.com/ETL-PIP/Pipline/blob/main/imgs/arch.png)
## Must be you have docker for run containers
* install docker-descktop  [link](https://docs.docker.com/desktop/install/ubuntu/).

## Getting started
* At first you'll need to get the source code of the project. Do this by cloning the [ETL-PIP](https://github.com/ETL-PIP/Pipline).
```
git clone https://github.com/ETL-PIP/Pipline.git
```
* navigate to path the project
```
cd Pipline
```

* add execution permission a file entrypoint.sh
```
chmod +x /script/entrypoint.sh
```
* install images and run containers on docker 
```
docker-compose up
```

* Create the .env File
### MongoDB Connection URI
MONGO_URI="mongodb+srv://admin:your_mongodb_password@cluster0.mongodb.net/?retryWrites=true&w=majority"

### MySQL Configuration
MYSQL_HOST="mysql_container"   # The MySQL container name (ensure Docker setup aligns with this)
MYSQL_USER="admin"             # MySQL username
MYSQL_PASSWORD="your_mysql_password"
MYSQL_DATABASE="mydatabase"

### Directory for JSON/SQLite files
DATA_DIR="/opt/airflow/dags/data/"

## Prerequisites

- Docker
- Docker Compose
- Python 3.8+
- Apache Airflow
- MongoDB Atlas
- MySQL database

**Airflow DAG (`dags/pipeline_dag.py`)**

![architecture](https://github.com/ETL-PIP/Pipline/blob/main/imgs/Dag.png)

**dashboard the airflow for monitoring**

![architecture](https://github.com/ETL-PIP/Pipline/blob/main/imgs/dash.png)

**data the all resources in data warehouse**

![architecture](https://github.com/ETL-PIP/Pipline/blob/main/imgs/mongo.png)