import boto3
import json
import os

def get_secret():
    secret_name = os.environ['SECRETNAME']
    secret_region = os.environ['SECRETREGION']
    
    client = boto3.client(service_name='secretsmanager',region_name=secret_region)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise e