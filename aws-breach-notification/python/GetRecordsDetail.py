import json
import os

def get_Records_detail(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "HostedZoneId": event['detail']['requestParameters']['hostedZoneId'],
            "Record_name" : event['detail']['requestParameters']['changeBatch']['changes'][0]['resourceRecordSet']['name']
        }
        event_details.append(detail)
    return event_details
    