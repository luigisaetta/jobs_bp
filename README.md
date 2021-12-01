# OCI Data SCience JOBS Best Practices
This repository contains a set of examples, with best practices for using **Data Science Jobs**

In OCI Data Science you can execute your Python code, for example to train a ML model, interactively using Notebook Sessions.
But very often you want to run that code in "batch mode", in order to be able to execute every time exactly the same steps.

In OCI Data Science you can launch:
* OCI DataFlow application, based on Apache Spark
* OCI DataScience JOBS.

With **Data Science JOBS** you can do in batch mode: 
* Data Preparation
* Training of a ML model
* Validation
* Scoring.

## Features
* How to launch a JOB using **REST API**
* How to launch a JOB using Oracle **ADS**
* How to use **ocifs** for reading from and writing to Object Storage
* How to use Resource Principal
* How to do batch scoring using JOBS

## Examples
* [utils.py](./utils.py) with examples on how to use ocifs
* Launch a JOB using REST API: [here.](./test_invoke_job_run.ipynb)
* Get the list of defined JOBS using ADS: [here.](./test_jobs_ads.ipynb)
* [Example](./test30.py) of a Python script using JOBS to do: loading of data, training of ML model, saving the model to Model Catalog
* [Example](./run_job_using_ads.ipynb) showing how to launch a JOB using Oracle **ADS**
* [Batch scoring using a JOB](./jobs_scoring_tutorial.md)

## Documentation
I have put some notes and best practices: [here.](./bp.md)

