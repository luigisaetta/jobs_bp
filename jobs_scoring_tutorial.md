# Scoring using Data Science (DS) JOBS

### Introduction
In this tutorial we assume that you have already trained a ML model and that you have saved the model in the Model Catalog.

We are going to see, step by step, how to do **"scoring in batch mode"**. 

In other words, how to use DS JOBS to do predictions on an input dataset.

We will assume that:
* The Model has been trained and saved to the Model Catalog.
* The dataset on which we want to do scoring is saved in a bucket on the Object Storage
* The predictions will be saved to the Object Storage
* Everything has been configured in order to have Resource Principal working
* We're using a Data Science Conda environment (for this example tf27_p37)
* We know how the "ML model internally works". In other words, how to use the artifacts we're downloading from the Model Catalog.

### Model validation
Well, it is easy to understand that the same example, with small changes, can be used to do Model Validation.
In this case you want to do predictions on a **test dataset** and compute some metrics (accuracy, AUC, ...) to verify, for example, that performances of your model have not degraded.

### Conda environments
The Conda environment we're using is one of the environment built-in Oracle Data Science, the one identified by the "slug" **tensorflow27_p37_cpu_v1**

But you can use any other environment, even a custom environment (that has been published). You need only to verify that the **oci** and **ads** versions are enough new.

* ads version >= 2.5.0

### Dataset used
The dataset used is orcl_attrition.csv

### Custom environment variables
To launch correctly the JOB we need to specify the followings environment variables:

```
CONDA_ENV_TYPE = service
CONDA_ENV_SLUG = tensorflow27_p37_cpu_v1
JOB_RUN_ENTRYPOINT = test_scoring.py
```

### Steps

In the code of the main py files (**test_scoring.py**) you need to put the code for the following steps:

1. Download the dataset from the Object Storage
2. Download Model's artifacts from the Model Catalog
3. Instantiate the model
4. (Eventually) Preprocess the input data
5. Do the scoring
6. Save the predictions (results) to the Object Storage

### Download the input dataset from the Object Storage
To make it easy to access the Object Storage, we're going to use **ocifs**

I have provided some utility fuctions in utils.py, that will be packed in our JOB code (with a zip).

The function that will be used is: read_from_object_storage, that return the data as a **Pandas** DataFrame.

```
print("Reading input dataset...")
data_orig = read_from_object_storage(PREFIX_INPUT, INPUT_FILE_NAME)
```

### Download Model's artifacts from the Model Catalog
```
ads.set_auth(auth='resource_principal')

mc = ModelCatalog(compartment_id=COMPARTMENT_OCID)

dl_model_artifact = mc.download_model(MODEL_OCID, DOWNLOAD_DIR, force_overwrite=True)

# check that the model pkl is there
if os.path.isfile(DOWNLOAD_DIR + "/" + MODEL_FILE):
    print ("Model file is there")
else:
    print ("Model file not exist")
```

### Save the predictions to the Object Storage

```
data_output.to_csv(OUTPUT_FILE_NAME, index=False)

print("Saving predictions to Object Storage...")

write_to_object_storage(PREFIX_OUTPUT, OUTPUT_FILE_NAME)
```

### zip the file for the JOB
The command used to create the zip file is:

```
zip test_scoring.zip -j -@ < scoring.lst
```

where scoring.lst contains (one by row) the list of the files we want to pack

### The complete example
The complete example is here: [test_scoring.py](./test_scoring.py)