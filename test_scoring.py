import oci
import ads
import os
import json

from ads import set_auth
from oci.auth.signers import get_resource_principals_signer
from ads.common.model_artifact import ModelArtifact
from ads.catalog.model import ModelCatalog

import pandas as pd
import numpy as np
import pickle

# from the utils file we have built
from utils import read_from_object_storage, write_to_object_storage

#
# constants
#
# remember the / at the end
PREFIX_INPUT = "oci://data_input@fr95jjtqbdhh/"
PREFIX_OUTPUT = "oci://data_output@fr95jjtqbdhh/"

INPUT_FILE_NAME = "orcl_attrition.csv"
OUTPUT_FILE_NAME = "scoring.csv"

COMPARTMENT_OCID = "ocid1.compartment.oc1..aaaaaaaaoxmcrbf3x3kozxkehlontyvtb4vif64vedvkneqv3b6rozumpxzq"
MODEL_OCID = "ocid1.datasciencemodel.oc1.eu-frankfurt-1.amaaaaaa7egirmqa2snieykohpie22i6vzdvelzmosvl52pnnrsgqtizot7q"
MODEL_FILE = "model.pkl"
DOWNLOAD_DIR = "./model"

N_INPUT_COLUMNS = 36

#
# main
#
print("Starting the JOB...")

# 1. Download the dataset from the Object Storage
print("Reading input dataset...")
data_orig = read_from_object_storage(PREFIX_INPUT, INPUT_FILE_NAME)

# test if reading OK
print('Input dataset shape is:', data_orig.shape)

# 2. Download Model's artifacts from Model Catalog
# for ADS we need to set RP as AUTH
ads.set_auth(auth='resource_principal')

mc = ModelCatalog(compartment_id=COMPARTMENT_OCID)

dl_model_artifact = mc.download_model(MODEL_OCID, DOWNLOAD_DIR, force_overwrite=True)

# check that the model pkl is there
if os.path.isfile(DOWNLOAD_DIR + "/" + MODEL_FILE):
    print ("Model file is there")
else:
    print ("Model file not exist")

# 3. Istantiate the model
# this step is made by code that depends on the ML libraries used. The model used inthe test was built using catboost
# you need to ensure that the required ML libraries are in the CONDA environment used to run the JOB (in this test tf27)
print("Instantiating the model...")

# simulate, not needed for the purpouse of the tutorial
print("Model instantiated..")

# 4. Preprocess input data
# steps here are dependant from the Model... and what kind of checks you want to do.
# Here I'll check only that we have the expected number of features in input
print("Preprocessing input data")

assert (data_orig.shape[1] == N_INPUT_COLUMNS)

# preparing for output
data_output = data_orig.copy()

# 5. do the scoring
# steps here are dependant from the Model...
# again, simulating it
print("Scoring")

data_output['score'] = 1

# saving locally
data_output.to_csv(OUTPUT_FILE_NAME, index=False)

# 6. Save predictions to Object Storage
print("Saving predictions to Object Storage...")

write_to_object_storage(PREFIX_OUTPUT, OUTPUT_FILE_NAME)

print("JOB finished.")


