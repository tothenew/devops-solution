import json
import os

def get_vpc_detail_create(event, context):

    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            'ResourceName': event['detail']['responseElements']['vpc']['vpcId']
        }
        event_details.append(detail)
    return event_details

def get_vpc_detail_delete(event, context):

    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            'ResourceName': event['detail']['requestParameters']['vpcId']
        }
        event_details.append(detail)
    return event_details