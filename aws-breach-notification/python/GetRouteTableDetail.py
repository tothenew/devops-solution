import json
import os

def get_route_table_detail_create(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "VPCID": event['detail']['responseElements']['routeTable']['vpcId'],
            "RouteTableID" : event['detail']['responseElements']['routeTable']['routeTableId']
        }
        event_details.append(detail)
    return event_details

def get_route_table_detail_delete(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "RouteTableID" : event['detail']['requestParameters']['routeTableId']
        }
        event_details.append(detail)
    return event_details