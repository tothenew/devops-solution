import json
import os

def get_endpointdetail(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "VpcEndpointId": event['detail']['requestParameters']['DeleteVpcEndpointsRequest']['VpcEndpointId']['content']
        }
        event_details.append(detail)
    return event_details