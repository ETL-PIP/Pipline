# Pipline
building a data pipeline with Apache Airflow to load data from multiple sources into a data warehouse 

## Must be you have docker for run containers
* install docker-descktop  [link](https://docs.docker.com/desktop/install/ubuntu/).

## Getting started
* At first you'll need to get the source code of the project. Do this by cloning the [ETL-PIP](https://https://github.com/ETL-PIP/Pipline.git).
```
git clone https://github.com/ETL-PIP/Pipline.gitcd ML-system-recommendation
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