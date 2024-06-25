import datetime
from elasticsearch import Elasticsearch
import uuid
import os
import base64
import json
import gzip
import logging
import boto3

def putMetricData(rds_instance_id, customMetricName, slow_queries_count):

    cloudWatchClient = boto3.client('cloudwatch', region_name="ap-south-1")
    response = cloudWatchClient.put_metric_data(
        Namespace='Custom/RDS-SlowQueries',
        MetricData=[
            {
                'MetricName': customMetricName,
                'Dimensions': [
                    {
                        'Name': 'DBInstanceIdentifier',
                        'Value': rds_instance_id
                    },
                    
                ],
                'Value': slow_queries_count,
                'Unit': 'Count'
            }
        ]
    )

def lambda_handler(event, context):
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(event)
    esHost = os.environ['ELASTICSEARCH_HOST']
    esPort = os.environ['ELASTICSEARCH_PORT']
    customMetricName="SlowQueriesCount"

    # Set your threshold for slow query execution time in seconds
      
    try:
        if 'awslogs' in event:
            if 'data' in event['awslogs']:
                eventData=base64.b64decode(event['awslogs']['data'])
                dataJson = json.loads(gzip.decompress(eventData))
                if 'messageType' in dataJson and dataJson['messageType']=='DATA_MESSAGE':
                    logGroup=dataJson['logGroup']
                    data=dataJson['logEvents']
                    function_name= logGroup.replace('/', '-').lower()
                    logger.info(function_name)
                    logger.info(data)
                    es = Elasticsearch([{'host': esHost, 'port': esPort}])
                    date = datetime.datetime.now().date()
                    es_index = function_name
                    if not es.indices.exists(index=str(es_index)+'-cwlogs' +'-'+str(date)):
                        es.indices.create(index=str(es_index)+'-cwlogs' +'-'+str(date), ignore=400)
                        logger.info(str(es_index)+'-cwlogs' +'-'+str(date)+' created')
                    cloudwatch_message = ""
                    slow_queries_count=0
                    for cdata in data:
                        esdata = {
                            "@timestamp":datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + 'Z',
                            "log": cdata['message'],
                            "hostname":es_index,
                            "app-type":es_index
                        }
                        cloudwatch_message = cloudwatch_message + str(cdata['message'])
                        response = es.index(index=str(es_index)+'-cwlogs' +'-'+str(date),id=uuid.uuid4(),body=esdata)
                        slow_queries_count+=1
                    logger.info(slow_queries_count)
                    putMetricData(es_index, customMetricName, slow_queries_count)
                        
                    queue_msg = {
                        "@timestamp":datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + 'Z',
                        "data": cloudwatch_message
                    }
                    
                    


    except Exception as e:
        logger.info(e)
        raise Exception(e)
    
      
   
    
    
