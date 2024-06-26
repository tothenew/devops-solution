def get_rds_modify_snapshot_public(event, context):
    event_details = []
    if "requestParameters" in event['detail']:
        request_parameters = event['detail']["requestParameters"]
        resource_name = ""
        if event['detail']['eventName'] == "ModifyDBClusterSnapshotAttribute":
            resource_name = event['detail']['requestParameters']['dBClusterSnapshotIdentifier']
        elif event['detail']['eventName'] == "ModifyDBSnapshotAttribute":
            resource_name = event['detail']['requestParameters']['dBSnapshotIdentifier']
        if "attributeName" in request_parameters and request_parameters["attributeName"] == "restore":
            public_allow = False
            resource_value = ""
            if "valuesToAdd" in request_parameters:
                values_to_add = request_parameters["valuesToAdd"]
                if values_to_add:
                    public_allow = True
                    resource_value = ', '.join(values_to_add)
            if public_allow:
                detail={
                    "SourceIPAddress": event['detail']["sourceIPAddress"],
                    "EventSource": event['detail']['eventSource'],
                    "EventName": event['detail']['eventName'],
                    'ResourceName': resource_name,
                    'ResourceValue': resource_value
                }
                event_details.append(detail)
    return event_details