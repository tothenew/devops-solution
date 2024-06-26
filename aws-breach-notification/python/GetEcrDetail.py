import json
import os

def get_ecr_detail(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "RepositoryName": event['detail']['responseElements']['repository']['repositoryName']
        }
        event_details.append(detail)
    return event_details
