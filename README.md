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

### 1. **Airflow DAG (`dags/pipeline_dag.py`)**

*The core of the ETL process is orchestrated with **Apache Airflow**. The pipeline is defined in the file `dags/pipeline_dag.py`, which contains several tasks:

![architecture](https://github.com/ETL-PIP/Pipline/blob/main/imgs/Dag.png)

*dashboard the airflow for monitoring

![architecture](https://github.com/ETL-PIP/Pipline/blob/main/imgs/dash.png)

*data the all resources in data warehouse

![architecture](https://github.com/ETL-PIP/Pipline/blob/main/imgs/mongo.png)