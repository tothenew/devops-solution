
import json
import os

def get_backupplan_detail(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "BackupPlanId": event['detail']['responseElements']['backupPlanId'],
        }
        event_details.append(detail)
    return event_details