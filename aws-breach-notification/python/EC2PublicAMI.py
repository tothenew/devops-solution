def get_ec2_modify_image_public(event, context):
    event_details = []
    if "requestParameters" in event['detail']:
        request_parameters = event['detail']["requestParameters"]
        if "launchPermission" in request_parameters:
            if "add" in request_parameters["launchPermission"]:
                if "items" in request_parameters["launchPermission"]["add"]:
                    items = request_parameters["launchPermission"]["add"]["items"]
                    public_allow = False
                    resource_value = ""
                    for item in items:
                        if "userId" in item:
                            public_allow = True
                            resource_value = item["userId"]
                    if public_allow:
                        detail={
                            "SourceIPAddress": event['detail']["sourceIPAddress"],
                            "EventSource": event['detail']['eventSource'],
                            "EventName": event['detail']['eventName'],
                            'ResourceName': event['detail']['requestParameters']['imageId'],
                            'ResourceValue': resource_value
                        }
                        event_details.append(detail)
    return event_details