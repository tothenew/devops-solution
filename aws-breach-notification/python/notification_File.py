import json
import time 
from urllib import request
import os

class Notification:  
  def __init__(self):
    self._account_name = os.environ['ACCOUNTNAME']
    self._layer_version= os.environ['LAYERVERSION']
    self._mail_ids = os.environ['EMAILIDS']

  def set_account_id(self, account_id):
    self._account_id = account_id

  def set_user_type(self, user_type):
    self._user_type = user_type
  
  def set_user(self, user):
    self._user = user

  def set_event_region(self, event_region):
    self._event_region = event_region

  def set_event_name(self, event_name):
    self._event_name = event_name

  def set_event_id(self, event_id):
    self._event_id = event_id

  def set_event_time(self, event_time):
    self._event_time = event_time
  
  def set_event_details(self, event_details):
    if type(event_details) != list:
      raise ValueError('event_details should be of tuple type')
    self._event_details = event_details
  def set_event_type(self,event_type):
    self._event_type = event_type

  def _generate_payload(self, event_type,accountname,layerversion, mail_ids):
    self._payload = {
      "type": event_type,
      "payload": {
        
        "AWSAccountID": self._account_id,
        "AccountName": accountname,
        "User": self._user,
        "UserType": self._user_type,
        "EventRegion": self._event_region,
        "EventMetaData": {
          "EventName": self._event_name,
          "EventTime": self._event_time,
          "EventID": self._event_id
        },
        "EventDetails": self._event_details,
        "MailRecipientIDs": mail_ids.split(','),
        "AgentDetails": {
          "LayerVersion": layerversion
        }
      }
    }
  def set_event_title(self):
      title = ""
      for detail in  self._event_details:
          if self._event_name == 'AuthorizeSecurityGroupIngress':
              title += "SG Inbound Port "+ str(detail["FromPort"])+" - "+str(detail["ToPort"])+" opened for "+str(detail["ipRange"])+" in security group "+str(detail["ResourceID"])+"\n"
          elif self._event_name == 'AuthorizeSecurityGroupEgress':
              title += "SG Outbound Port "+ str(detail["FromPort"])+" - "+str(detail["ToPort"])+" opened for "+str(detail["ipRange"])+" in security group "+str(detail["ResourceID"])+"\n"
          elif self._event_name == 'ConsoleLogin':
              if detail['ConsoleLoginResponse'] == "Failure":
                  title += "Somebody tried to login through Aws console using "+str(self._user)+" user credential and failed, MFA enabled: "+detail['MFAUsed']+", source ip: "+str(detail['SourceIPAddress'])+"\n"
              elif detail['ConsoleLoginResponse'] == "Success" and self._user == "Root":
                  title += "Somebody just loggedin through Aws console using Root user access, MFA enabled: "+detail['MFAUsed']+",  source ip: "+str(detail['SourceIPAddress'])+"\n"
              elif detail['ConsoleLoginResponse'] == "Success" and self._user != "Root" and detail['MFAUsed'] == "No":
                  title += "Somebody just loggedin through Aws console without MFA enabled using "+str(self._user)+" user credential, source ip: "+str(detail['SourceIPAddress'])+"\n"
          elif self._event_name == 'CreateAccessKey':
              title += "Access key has been generated for user "+detail["KeyGeneratedFor"]+"\n"
          elif self._event_name == 'PutBucketPublicAccessBlock':
              title += "S3 Bucket Public Access opened for bucket "+str(detail['ResourceName'])+",  source ip: "+str(detail['SourceIPAddress'])+"\n"
          elif self._event_name == 'PutBucketAcl':
              title += "S3 Bucket Public Access opened for bucket "+str(detail['ResourceName'])+",  source ip: "+str(detail['SourceIPAddress'])+"\n"
          elif self._event_name == "DeleteTrail":
              title += "CloudTrail trail "+str(detail['ResourceName'])+" has been deleted"+"\n"
          elif self._event_name == "StopLogging":
              title += "CloudTrail trail "+str(detail['ResourceName'])+" is stop logging"+"\n"
          elif self._event_name == "CreateFunction20150331":
              title += "New account on boarded\n"
          elif self._event_name == "UpdateFunctionCode20150331v2":
              title += "Client function code updated\n"
          elif self._event_name == "UpdateFunctionConfiguration20150331v2":
              title += "Client function configuration updated\n"
          elif self._event_name == 'ModifySnapshotAttribute':
              title += "EC2 Snapshot Public Access open for snapshot id "+str(detail['ResourceName'])+", source ip: "+str(detail['SourceIPAddress'])+"\n"
          elif self._event_name == 'ModifyImageAttribute':
              title += "EC2 AMI Public Access open for image id "+str(detail['ResourceName'])+", source ip: "+str(detail['SourceIPAddress'])+"\n"
          elif self._event_name == 'RunInstances':
              title += "EC2 Instance Public Access open for instance id "+str(detail['ResourceName'])+", source ip: "+str(detail['SourceIPAddress'])+"\n"
          elif self._event_name == 'ModifyDBClusterSnapshotAttribute' or self._event_name == 'ModifyDBSnapshotAttribute':
              title += "RDS Snapshot Public Access open for snapshot name "+str(detail['ResourceName'])+", source ip: "+str(detail['SourceIPAddress'])+"\n"
          elif self._event_name == 'CreateDBInstance':
              title += "RDS Instance Public Access open for database name "+str(detail['ResourceName'])+", source ip: "+str(detail['SourceIPAddress'])+"\n"
          elif self._event_name == 'DeleteAccessKey':
              title += "Access key has been Deleted for user "+detail["KeyGeneratedFor"]+"\n"
          elif self._event_name == 'CreateLoadBalancer':
              title += "New Pubic Loadbalancer " +detail["ResourceName"]+ " has been created " +"\n"
          elif self._event_name == 'CreateVpc':
              title += "New Vpc " +detail["ResourceName"]+ "has been created " +"\n"
          elif self._event_name == 'DeleteVpc':
              title += "Vpc " +detail["ResourceName"]+ " has been deleted " +"\n"
          elif self._event_name == 'CreateSubnet':
              title += "Subnet "+ detail["SubnetName"]+ " has been created  "+ "\n"      
          elif self._event_name == 'DeleteSubnet':
              title += "Subnet "+ detail["SubnetID"]+ " has been deleted  "+ "\n"  
          elif self._event_name == 'CreateNatGateway':
              title += "Nat Gateway "+ detail["NatGatewayID"]+ " has been created in  " + detail["SubnetID"]+ "\n" 
          elif self._event_name == 'DeleteNatGateway':
              title += "Nat Gateway "+ detail["NatGatewayID"]+ " has been deleted in " + detail["SubnetID"]+ "\n" 
          elif self._event_name == 'CreateRouteTable':
              title += "Route table "+ detail["RouteTableID"]+ " has been created in " + detail["VPCID"]+ "\n" 
          elif self._event_name == 'DeleteRouteTable':
              title += "Route table "+ detail["RouteTableID"]+ " has been deleted "+ "\n"
          elif self._event_name == 'DeleteHostedZone':
              title += "Hosted Zone "+ detail["HostedZoneName"]+ " has been deleted " + "\n" 
          elif self._event_name == 'ChangeResourceRecordSets':
              title += "Record "+ detail["Record_name"]+ " has been deleted in hosted zone " + detail["HostedZoneId"]+ "\n" 
          elif self._event_name == 'DeleteSecret':
              title += "Secret "+ detail["ResourceName"]+ " has been deleted  " + "\n" 
          elif self._event_name == 'DeleteBackupPlan':
              title += "Backup plan "+ detail["BackupPlanId"]+ " has been deleted " + "\n" 
          elif self._event_name == 'DeleteBackupVault':
              title += "Backup vault "+ detail["BackupVaultName"]+ " has been deleted "  + "\n"   
          elif self._event_name == 'CreateVpcPeeringConnection':
              title += "Vpc peering "+ detail["ResourceName"]+ " has been created "  + "\n" 
          elif self._event_name == 'DeleteVpcPeeringConnection':
              title += "Vpc peering "+ detail["ResourceName"]+ " has been deleted "  + "\n" 
          elif self._event_name == 'CreateRepository':
              title += "Public Ecr repo "+ detail["RepositoryName"]+ " has been created  "  + "\n" 
          elif self._event_name == 'CreateNetworkAcl':
              title += "Nacl "+ detail["NaclID"]+ " has been created "  + "\n" 
          elif self._event_name == 'DeleteNetworkAcl':
              title += "Nacl "+ detail["NaclID"]+ " has been deleted "  + "\n" 
          elif self._event_name == 'AllocateAddress':
              title += "Elastic ip with allocation id  "+ detail["AllocationId"]+ " has been created"  + "\n"   
          elif self._event_name == 'DeleteVpcEndpoint':
              title += "Vpc Endpoint with id "+ detail["VpcEndpointId"]+ " has been created "  + "\n"
          elif self._event_name == 'ReleaseAddress':
              title += "Elastic ip with allocation id "+ detail["AllocationId"]+ " has been deleted "  + "\n"                  

      self._event_title = title

def evaluate(event, event_details):
  if type(event_details) == list and len(event_details) > 0:
    notification = Notification()
    notification.set_account_id(event['detail']['userIdentity']["accountId"])
    notification.set_user_type(event['detail']['userIdentity']['type'])
    
    if notification._user_type == "Root":
      username = "Root"
    else:
      username = event['detail']['userIdentity']['arn'].split('/')[-1]
    notification.set_user(username)

    notification.set_event_region(event['detail']["awsRegion"])
    notification.set_event_name(event['detail']['eventName'])
    notification.set_event_id(event['id'])
    notification.set_event_time(event['time'])
    notification.set_event_details(event_details)
    notification.set_event_title()
    
    if event['detail']['eventName'] in ["CreateFunction20150331","UpdateFunctionConfiguration20150331v2", "UpdateFunctionCode20150331v2"]:
      notification.set_event_type("info")
    else:
      notification.set_event_type("event")
    return notification