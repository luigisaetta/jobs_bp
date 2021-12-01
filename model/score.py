
#
# customize and save score.py
#
import pandas as pd
import numpy as np
import time

import catboost as cat

import pickle
import json
import os
import io
import logging 

# logging configuration - OPTIONAL 
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger_pred = logging.getLogger('model-prediction')
logger_pred.setLevel(logging.INFO)
logger_feat = logging.getLogger('input-features')
logger_feat.setLevel(logging.INFO)

# it is loaded in load_model()
model_file_name = "model.pkl"

# to enable/disable detailed logging
DEBUG = True

"""
   Inference script. This script is used for prediction by scoring server when schema is known.
"""

def load_model():
    """
    Loads model from the serialized format

    Returns
    -------
    model:  a model instance on which predict API can be invoked
    """
    
    model_dir = os.path.dirname(os.path.realpath(__file__))
    contents = os.listdir(model_dir)
    
    # Load the model from the model_dir using the appropriate loader
    
    if model_file_name in contents:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), model_file_name), "rb") as file:
            model = pickle.load(file) 
            logger_pred.info("Loaded model...")
       
    else:
        raise Exception('{0} is not found in model directory {1}'.format(model_file_name, model_dir))
    
    return model

def preprocess_data(x):
    logger_pred.info("Eventually preprocessing and adding features...")
    
    return x

def predict(data, model=load_model()) -> dict:
    """
    Returns prediction given the model and data to predict

    Parameters
    ----------
    model: Model instance returned by load_model API
    data: Data format as expected by the predict API of the core estimator. For eg. in case of sckit models it could be numpy array/List of list/Panda DataFrame

    Returns
    -------
    predictions: Output from scoring server
        Format: { 'prediction': output from `model.predict` method }

    """
    # model contains the model and the scaler
    logger_pred.info("In predict...")
    
    # some check
    assert model is not None, "Model is not loaded"
    
    x = pd.read_json(io.StringIO(data)).values
    
    if DEBUG:
        logger_feat.info("Logging features")
        logger_feat.info(x)
    
    # preprocess data (for example normalize features)
    x = preprocess_data(x)

    logger_pred.info("Invoking model......")
    
    preds = model.predict_proba(x)
    
    # rounded
    preds = np.round(preds[:, 1], 4)
    preds = preds.tolist()
    
    logger_pred.info("Logging predictions")
    logger_pred.info(preds)
    
    return { 'prediction': preds }
