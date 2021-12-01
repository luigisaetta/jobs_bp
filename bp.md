# Some notes and best practices on DS JOBS

#### Author:      L. Saetta
#### Last update: 30/11/2021

### JOBS types

OCI Data Science can run two types of JOBS:
* Infrastructure JOBS (normally called JOBS)
* DataFlow JOBS, run in OCI DataFlow (based on Apache Spark)

### Resource Principal

In a DS JOB you most probably (or surely) need to access to other Cloud resources (for example: Object Storage)

The simplest way of doing this is to use **Resource Principal (RP)**.

To be able to use Resource Principal, the easy way is to add Data Science JOBs, defined in the compartment you're working with, in the same **Dynamic Group** you're using for Notebooks' Sessions.

You need to add a rule like this one to the definition of your dynamic group:

```
all {resource.type='datasciencejobrun', resource.compartment.id= 'ocid1.compartment.oc1..aaaaaaaaoxmcrbf3x3kozxkehlontyvtb4vif64vedvkneqv3b6rozumpxzq'}
```

### Get the Resource Principal Signer

In a Notebook, you can use this code:

```
rps = oci.auth.signers.get_resource_principals_signer()
```

### How to get IDs in a Notebook Session

When you want to launch a JOB you need to know:
* compartId: the Id of the OCI compartment containing the JOB
* project Id

You can get these information in a Notebook running in the same compartment/project, using this code:

```
import os

print('The identifier (name) of the OCI region is:', os.environ["NB_REGION"])
print('The Tenancy OCID is:', os.environ["TENANCY_OCID"])
print()
print('The Notebook Session Compartment OCID is:', os.environ["NB_SESSION_COMPARTMENT_OCID"])
print()
print('The Project OCID is:', os.environ["PROJECT_OCID"])
print()
```

### Using CONDA Environments

Usually, when you want to launch a JOB run you want to use exactly the same CONDA env you have used in a Notebook.

For example, you have trained a ML model in a Notebook and you have used the CONDA env "tensorflow27_p37_cpu_v1". 

If you want to repeat several times the training, in batch mode, you can reuse the code in a JOB, but you want to ensure that you're using, every time, exactly the same CONDA env, with the same libraries' versions.

You can easily control this thing using JOBS. When you create a JOB you can specify the values for several environment variables.

In this case you have to specify:

```
CONDA_ENV_TYPE = service
CONDA_ENV_SLUG = tensorflow27_p37_cpu_v1
```

**Service** can be use for CONDA envs provided by Oracle Data Science.


### How to read a CSV file directly from Object Storage using ocfs

[ocifs](https://docs.oracle.com/en-us/iaas/tools/ocifs-sdk/latest/index.html) is a library, provided from Oracle Data Science team, that enables you to easily access the **Object Storage** as if it were a file system.

Using the function **read_from_object_storage**, provided in utils.py, you can read a CSV file, stored on the Object Storage, in a **Pandas DataFrame**.

```
def read_from_object_storage(prefix, file_name):
    # get access to OSS as an fs
    # config={} assume RESOURCE PRINCIPAL auth
    fs = ocifs.OCIFileSystem(config={})
    
    FILE_PATH = prefix + file_name
    
    # reading data from Object Storage
    with fs.open(FILE_PATH, 'rb') as f:
        df = pd.read_csv(f)
    
    return df
```

In utils.py you can find also an example, useful to **write** a binary file (for example the model file) to Object Storage.

If you want to use in the JOB the Resource Principal way of **handling security**, you need:
* add the JOBS to the Dynamic Group
* add proper policies for Object Storage access to the Dynamic Group

### Pipelines

You can launch a DS JOB using the REST API ([see](./test_invoke_job_run.ipynb)).

In OCI Data Integration you can use **REST task** to invoke a REST service. Therefore you can include in a OCI DI pipeline the call to launch a DS Job.

### Zip file

It is possible to create a JOB from a **zip** file containing multiple .py files (+ additional files).

In this case, when you create the JOB you have to specify

```
JOB_RUN_ENTRYPOINT = <name of main py file>
```

If you create a zip file without sub-directories, your files will be put in

```
PATH_DECOMPRESSED = "/home/datascience/decompressed_artifact"
```

[test40.py](./test40.py) is an example that you can use if you want to add a custom score.py (useful for Model deployment)

Another example where you need to use a zip file is when you need to access **ADWH**. In this situation you need to add to your files the wallet.
