import json
import os

def get_hostedZone_detail(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "HostedZoneName": event['detail']['requestParameters']['id']
        }
        event_details.append(detail)
    return event_details