import json
import os

def get_secret_detail(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "ResourceName" : event['detail']['responseElements']['name']
        }  
        event_details.append(detail)
    return event_details