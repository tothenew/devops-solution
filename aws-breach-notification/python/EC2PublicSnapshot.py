def get_ec2_modify_snapshot_public(event, context):
    event_details = []
    if "requestParameters" in event['detail']:
        request_parameters = event['detail']["requestParameters"]
        if "createVolumePermission" in request_parameters:
            if "add" in request_parameters["createVolumePermission"]:
                if "items" in request_parameters["createVolumePermission"]["add"]:
                    items = request_parameters["createVolumePermission"]["add"]["items"]
                    public_allow = False
                    resource_value = ""
                    for item in items:
                        if "group" in item and item["group"] == "all":
                            public_allow = True
                            resource_value = item["group"]
                        elif "userId" in item:
                            public_allow = True
                            resource_value = item["userId"]
                    if public_allow:
                        detail={
                            "SourceIPAddress": event['detail']["sourceIPAddress"],
                            "EventSource": event['detail']['eventSource'],
                            "EventName": event['detail']['eventName'],
                            'ResourceName': event['detail']['requestParameters']['snapshotId'],
                            'ResourceValue': resource_value
                        }
                        event_details.append(detail)
    return event_details