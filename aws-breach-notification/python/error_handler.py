
import json
import time 
from urllib import request
import os

def send_message(event, event_region, account_id, message):
    layerversion = os.environ['LAYERVERSION']
    accountname = os.environ['ACCOUNTNAME']
    payload = generate_payload(accountname, layerversion, message, event, account_id, event_region)
    try:
        print("Sending error message with the following payload:")
        print(json.dumps(payload, indent=4))
    except Exception as e:
        logger.error("Failed to print message", exc_info=True)

def generate_payload(accountname, layerversion, message, event, account_id, event_region):
    return {
      "type": "error",
      "payload": {
        "AWSAccountID": account_id,
        "AccountName": accountname,
        "EventRegion": event_region,
        "EventDetails": {
            "Message": message,
            "Payload": event
        },
        "AgentDetails": {
          "LayerVersion": layerversion
        }
      }
    }