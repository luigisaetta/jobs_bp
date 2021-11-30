import oci
import ads
import os
import json
import tensorflow as tf

from ads import set_auth
from oci.auth.signers import get_resource_principals_signer
from oci.data_science import DataScienceClient
from ads.dataset.factory import DatasetFactory
from oci.object_storage import ObjectStorageClient
from ads.common.model_artifact import ModelArtifact
from ads.common.model_export_util import prepare_generic_model

import pandas as pd
import numpy as np
import pickle

from sklearn.linear_model import LogisticRegression

# functions to help
BUFFER_SIZE = 1024 * 1024

def download_file(namespace, bucket_name, file_name, rprinc_signer):
    os_client = oci.object_storage.ObjectStorageClient({}, signer=rprinc_signer)
    
    # save a file from object storage to local FS
    print()
    print('*** saving file to local FS...')
    get_obj = os_client.get_object(namespace, bucket_name, file_name)
    
    # legge il file da Obiect Storage e scrive, in chunck di dimensione BUFFER_SIZE
    with open(file_name, 'wb') as f:
        for chunk in get_obj.data.raw.stream(BUFFER_SIZE, decode_content=False):
            f.write(chunk)
#
# Main
#

# constant definition
# model file name
MODEL_FILE = 'logreg.pkl'

MODEL_DISPLAY_NAME = "logreg-model-new3-test-job"
MODEL_DESC = "A new logreg model new30 for testing jobs"

MAX_ITER = 1100

# directory
PATH_ARTEFACT = f"./model-files"

# definition of the CONDA env to use
CONDA_ENV_URL = 'oci://service-conda-packs@id19sfcrra6z/service_pack/cpu/TensorFlow 2.7 for CPU on Python 3.7/1.0/tensorflow27_p37_cpu_v1'
CONDA_ENV_SLUG = "tensorflow27_p37_cpu_v1"


print('*** Testing access to some libraries')

print("OCI SDK version:", oci.__version__)

print("TF version:", tf.__version__)

print("ADS version:", ads.__version__)

try:
    print()
    print('*** Testing access to Resource Principal')
    set_auth(auth='resource_principal')
    rps = get_resource_principals_signer() 
    
    print()
    print('*** Creating DataScience Client')
    dsc = DataScienceClient(config={}, signer=rps)
    
    print()
    print('*** Test access to Object Storage')

    namespace = "fr95jjtqbdhh"
    bucket_name = "data_input"
    file_name = "cs-training.csv"
    
    # download from OS and write to local FS
    download_file(namespace, bucket_name, file_name, rps)
    
    # now a sample of ML training... will keep simple: sklearn Logistic regression
    print()
    print('*** Now the ML...')
    
    # load file in a Pandas DataFrame
    data_orig = pd.read_csv(file_name)

    # data preprocessing
    # trattamento valori null
    data_orig['NumberOfDependents'] = data_orig['NumberOfDependents'].fillna(0)
    data_orig['MonthlyIncome'] = data_orig['MonthlyIncome'].fillna(-1)

    x_columns = ['RevolvingUtilizationOfUnsecuredLines', 'age',
       'NumberOfTime30-59DaysPastDueNotWorse', 'DebtRatio', 'MonthlyIncome',
       'NumberOfOpenCreditLinesAndLoans', 'NumberOfTimes90DaysLate',
       'NumberRealEstateLoansOrLines', 'NumberOfTime60-89DaysPastDueNotWorse',
       'NumberOfDependents']
    y_columns = ['SeriousDlqin2yrs']

    x_train = data_orig[x_columns].values

    y_train = data_orig[y_columns].values.ravel()
    

    # do the training
    print()
    print('*** do the Training...')
    
    # since the performance is not really important I'll avoid normalization
    clf = LogisticRegression(random_state=0, max_iter=MAX_ITER)

    clf.fit(x_train, y_train)

    if not os.path.exists(PATH_ARTEFACT):
        os.mkdir(PATH_ARTEFACT)

    # before pickle.dump
    # aggiunto model=clf, in questo modo specifico le info di tassonomia
    print()
    print('*** save the trained model to the model catalog...')
    
    # now I'm using the SLUG... it is OK
    artifact = prepare_generic_model(PATH_ARTEFACT, force_overwrite=True, model=clf, data_science_env=True,
                                 inference_conda_env = CONDA_ENV_URL)

    pickle.dump(clf, open(PATH_ARTEFACT + "/" + MODEL_FILE, 'wb'))
    
    # this code needs to be added for the JOB: mandatory
    compartment_ocid = os.environ.get("NB_SESSION_COMPARTMENT_OCID") if os.environ.get("NB_SESSION_COMPARTMENT_OCID") else os.environ.get("PROJECT_COMPARTMENT_OCID")

    catalog_entry = artifact.save(display_name=MODEL_DISPLAY_NAME, description=MODEL_DESC, compartment_id=compartment_ocid)
    
    # END
    print()
    print("Tests completed successfully!!!")
    
except Exception as e:
    print()
    print("Some exceptions occurred:", e)
