import json
import os

def get_natgateway_detail_create(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "NatGatewayID": event['detail']['responseElements']['CreateNatGatewayResponse']['natGateway']['natGatewayId'],
            "SubnetID" : event['detail']['responseElements']['CreateNatGatewayResponse']['natGateway']['subnetId'],
            "VpcId" : event['detail']['responseElements']['CreateNatGatewayResponse']['natGateway']['vpcId']
        }
        event_details.append(detail)
    return event_details

def get_natgateway_detail_delete(event, context):
    if 'detail' in event:
        event_details = []
        detail={
            "SourceIPAddress": event['detail']["sourceIPAddress"],
            "EventSource": event['detail']['eventSource'],
            "EventName": event['detail']['eventName'],
            "NatGatewayID": event['detail']['requestParameters']['DeleteNatGatewayRequest']['NatGatewayId']
            
        }
        event_details.append(detail)
    return event_details