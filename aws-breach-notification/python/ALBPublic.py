import time
import boto3

def get_alb_scheme(event, context):
    event_details = []
    if "requestParameters" in event['detail']:
        response_elements = event['detail']["requestParameters"]
        if "subnetMappings" in response_elements:
            ec2_client = boto3.client('ec2', region_name=event['detail']["awsRegion"])
            subnets = response_elements["subnetMappings"]
            for item in subnets:
                public_allow = False
                subnet_id = item['subnetId']
                response = ec2_client.describe_route_tables(Filters=[{"Name": "association.subnet-id", "Values": [subnet_id]}])
                if "RouteTables" in response:
                    print("route table in repopnse")
                    for route_table in response["RouteTables"]:
                        if "Routes" in route_table:
                            print("for one route table")
                            for route in route_table["Routes"]:
                                if "DestinationCidrBlock" in route and route["DestinationCidrBlock"] and route["DestinationCidrBlock"] == "0.0.0.0/0":
                                    if "GatewayId" in route and route["GatewayId"] and route["GatewayId"].startswith("igw-"):
                                        public_allow = True
                        print("public_allow", public_allow)                
                        if public_allow:
                            detail = {
                                "SourceIPAddress": event['detail']["sourceIPAddress"],
                                "EventSource": event['detail']['eventSource'],
                                "EventName": event['detail']['eventName'],
                                'ResourceName': event['detail']['requestParameters']['name'],
                                'ResourceValue': item['subnetId']
                            
                            }
                            event_details.append(detail)            
    
    return event_details