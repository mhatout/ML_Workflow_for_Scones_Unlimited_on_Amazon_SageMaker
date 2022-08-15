# Deploy and monitor a machine learning workflow for Image Classification

## Context
This project is a part of the Udacity's AWS ML Engineer Nanodegree Program.

## Scones Unlimited
The goal of the project is to build a ML Model that classify image through ML workflows using Amazon's Sage Maker. The Step Functions linked with the lambda scripts are used to automate various tasks of ML process from Data Preprocessing, Model Training, Deployment and Evaluating.

1. Lambda Function takes the address of an image hosted in S3, then serializes and returns a JSON object.
2. Lambda Function takes the JSON object returned from first function and passes it to the ML model endpoint and return the result as a JSON Object.
3. Lambda Function takes the inference data from second function and filters only the images that meet the defined confidence threshold.
