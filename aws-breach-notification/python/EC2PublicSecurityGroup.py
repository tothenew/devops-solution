import boto3

egress_white_list_port = [80, 443, 587]
ingress_white_list_port = [80, 443]


def is_public_allowed(message, public_allow, rule, rule_type):
    white_list_port = []
    if rule_type == "Ingress":
        white_list_port = ingress_white_list_port
    elif rule_type == "Egress":
        white_list_port = egress_white_list_port
    if rule['IpProtocol'] == "-1":
        public_allow = True
        message.add(rule_type)
    elif not rule["FromPort"] in white_list_port:
        public_allow = True
        message.add(rule_type)
    return public_allow


def get_ec2_public_security_group(event, context):
    event_details = []
    message = set()
    if "responseElements" in event['detail']:
        response_elements = event['detail']["responseElements"]
        public_allow = False

        security_group_id = response_elements["groupId"]

        ec2_client = boto3.client('ec2', region_name=event['detail']["awsRegion"])

        security_groups = ec2_client.describe_security_groups(GroupIds=[security_group_id])['SecurityGroups']

        for group in security_groups:
            if 'IpPermissions' in group:
                for rule in group['IpPermissions']:
                    if "IpRanges" in rule:
                        for ip_range in rule['IpRanges']:
                            if ip_range['CidrIp'] == '0.0.0.0/0':
                                public_allow = is_public_allowed(message, public_allow, rule, "Ingress")
                    if "Ipv6Ranges" in rule:
                        for ip_range in rule['Ipv6Ranges']:
                            if ip_range['CidrIpv6'] == '::/0':
                                public_allow = is_public_allowed(message, public_allow, rule, "Ingress")
            if 'IpPermissionsEgress' in group:
                for rule in group['IpPermissionsEgress']:
                    if "IpRanges" in rule:
                        for ip_range in rule['IpRanges']:
                            if ip_range['CidrIp'] == '0.0.0.0/0':
                                public_allow = is_public_allowed(message, public_allow, rule, "Egress")
                    if "Ipv6Ranges" in rule:
                        for ip_range in rule['Ipv6Ranges']:
                            if ip_range['CidrIpv6'] == '::/0':
                                public_allow = is_public_allowed(message, public_allow, rule, "Egress")

        if public_allow:
            detail = {
                "SourceIPAddress": event['detail']["sourceIPAddress"],
                "EventSource": event['detail']['eventSource'],
                "EventName": event['detail']['eventName'],
                'ResourceName': response_elements["groupId"],
                'ResourceValue': "Internet allowed in " + "and ".join(message)
            }
            event_details.append(detail)
    return event_details