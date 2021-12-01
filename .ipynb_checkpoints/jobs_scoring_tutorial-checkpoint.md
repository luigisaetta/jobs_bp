# Scoring using Data Science (DS) JOBS

### Introduction
In this tutorial we assume that you have already trained a ML model and that you have saved the model in the Model Catalog.

We are going to see, step by step, how to do **"scoring in batch mode"**. In other words, how to use DS JOBS to do predictions on an unput set of data.

We will assume that:
* the Model has been trained and saved to the Model Catalog.
* the dataset on which we want to do scoring is saved in a bucket on the Object Storage
* the predictions will be saved to the Object Storage
* everything has been configured in order to have Resource Principal working
* we're using a Data Science Conda environment (for this example tf27_p37)
* we know how the "ML model internally works". In other words, how to use the artifacts we're downloading from the Model Catalog.

### Steps

1. Download the dataset from the Object Storage
2. Download Model's artifacts from the Model Catalog
3. Instantiate the model
4. (Eventually) Preprocess the input data
5. Do the scoring
6. Save the predictions (results) to the Object Storage

