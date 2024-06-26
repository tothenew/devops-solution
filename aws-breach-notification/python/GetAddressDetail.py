
import json
import os

def get_address_create(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "AllocationId": event['detail']['responseElements']['allocationId'],
        }
        event_details.append(detail)
    return event_details

def get_address_delete(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "AllocationId": event['detail']['requestParameters']['allocationId'],
        }
        event_details.append(detail)
    return event_details    


