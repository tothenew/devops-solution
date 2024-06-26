import time
import boto3

def get_ec2_instance_public(event, context):
    event_details = []
    if "responseElements" in event['detail']:
        response_elements = event['detail']["responseElements"]
        if "instancesSet" in response_elements:
            instance_set = response_elements["instancesSet"]
            if "items" in instance_set:
                ec2_client = boto3.client('ec2', region_name=event['detail']["awsRegion"])
                for item in instance_set["items"]:
                    if "instanceId" in item:
                        instance_id = item["instanceId"]
                        subnet_id = item["subnetId"]
                        public_allow = False
                        response = ec2_client.describe_route_tables(Filters=[{"Name": "association.subnet-id", "Values": [subnet_id]}])
                        if "RouteTables" in response:
                            for route_table in response["RouteTables"]:
                                if "Routes" in route_table:
                                    for route in route_table["Routes"]:
                                        if "DestinationCidrBlock" in route and route["DestinationCidrBlock"] and route["DestinationCidrBlock"] == "0.0.0.0/0":
                                            if "GatewayId" in route and route["GatewayId"] and route["GatewayId"].startswith("igw-"):
                                                public_allow = True
                        if public_allow:
                            detail={
                                "SourceIPAddress": event['detail']["sourceIPAddress"],
                                "EventSource": event['detail']['eventSource'],
                                "EventName": event['detail']['eventName'],
                                'ResourceName': instance_id,
                                'ResourceValue': subnet_id
                            }
                            event_details.append(detail)
    return event_details