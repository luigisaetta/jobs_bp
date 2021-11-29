# Some notes and best practices on DS JOBS

### Author:      L. Saetta
### Last update: 29/11/2021

### Resource Principal
In a DS JOB you most probably (or surely) need to access to others Cloud resources (for example: Object Storage)

The simplest way of doing this is to use **Resource Principal (RP)**.

To be able to use Resource Principal, the easy way is to add Data Science JOBs, defined in the compartment you're working with, in the same **Dynamic Group** you're using for Notebooks Sessions.

You need to add a rule like this one to the definition of your dynamic group:

```
all {resource.type='datasciencejobrun', resource.compartment.id= 'ocid1.compartment.oc1..aaaaaaaaoxmcrbf3x3kozxkehlontyvtb4vif64vedvkneqv3b6rozumpxzq'}
```

### How to get IDs in a Notebook Session

When you want to launch a JOB you need to know:
* compartId: the Id of the compartment containing the JOB
* project Id

You can get these information in a Notebook running in the same compartment/project:

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