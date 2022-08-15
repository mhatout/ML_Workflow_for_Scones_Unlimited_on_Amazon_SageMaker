"""
serialize_image_data: Lambda function to pull an image from S3 and returning serializing data
"""

import json
import boto3
import base64

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']

    # Download the data from s3 to /tmp/image.png
    boto3.resource('s3').Bucket(bucket).download_file(key, '/tmp/image.png')

    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

"""
classify_image: Lambda function to predict image classification
"""

import json
import base64
import boto3

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2022-08-15-00-38-26-318"
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['image_data'])

    # Make a prediction:
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT,ContentType='image/png',Body=image)
    inferences = response['Body'].read().decode('utf-8')
    
    # We return the data back to the Step Function    
    event["inferences"] = json.loads(inferences)
    return {
        'statusCode': 200,
        'body': event
    }

"""
filter_inference_confidence : Lambda function to filter inference results based on confidence
"""

import json


THRESHOLD = 0.90


def lambda_handler(event, context):

    # Grab the inferences from the event
    inferences = event["inferences"]

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = any (x > THRESHOLD for x in inferences)

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

