import json
import os

def get_subnet_detail_create(event, context):
    if 'detail' in event:
        event_details = []
        subnet_name = None
        for item in event['detail']['responseElements']['subnet']['tagSet']['items']:
            if item['key'] == "Name":
                subnet_name = item['value']
            break
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "VPC-ID": event['detail']['responseElements']['subnet']['vpcId'],
            "SubnetName" : subnet_name
        }
        event_details.append(detail)
    return event_details

def get_subnet_detail_delete(event, context):
    if 'detail' in event:
        event_details = []
        
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "SubnetID" : event['detail']['requestParameters']['subnetId']
        }
        event_details.append(detail)
    return event_details