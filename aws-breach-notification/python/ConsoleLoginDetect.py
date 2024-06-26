import json
import os
def ConsoleLoginDetectHandler(event, context):
    mFAUsed = event['detail']["additionalEventData"]["MFAUsed"]
    userType = event['detail']['userIdentity']['type']
    loginResponse = event['detail']["responseElements"]["ConsoleLogin"]
    try:
        userName = event['detail']['userIdentity']['userName']
    except:
        userName = userType
    if 'detail' in event and loginResponse != "Failure"  and (mFAUsed == "No" or userType == "Root") and userType != "AssumedRole":
        event_details = []
        detail={
            'SourceIPAddress': event['detail']["sourceIPAddress"],
            'ConsoleLoginResponse': loginResponse,
            'MFAUsed': mFAUsed,
            'UserName': userName
        }
        event_details.append(detail)
        return event_details