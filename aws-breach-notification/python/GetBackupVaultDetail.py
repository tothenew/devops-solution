
import json
import os

def get_backupvault_detail(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "BackupVaultName": event['detail']['requestParameters']['backupVaultName'],
        }
        event_details.append(detail)
    return event_details