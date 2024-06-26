import json
import os

def get_nacl_detail_create(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "VPCID": event['detail']['responseElements']['networkAcl']['vpcId'],
            "NaclID" : event['detail']['responseElements']['networkAcl']['networkAclId']
        }
        event_details.append(detail)
    return event_details

def get_nacl_detail_delete(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "NaclID" : event['detail']['requestParameters']['networkAclId']
        }
        event_details.append(detail)
    return event_details