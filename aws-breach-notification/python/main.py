import traceback
import notification_File as notification
import eventPlaceEngine.ses as ses

########################### Main function for child account #######################
def main(event, context):
    try:
        if event['detail']['eventName'] in ['PutBucketPublicAccessBlock', 'PutBucketAcl']:
            PutBucketPublicAccessBlock(event, context)
        elif event['detail']['eventName'] == 'AuthorizeSecurityGroupIngress':
            AuthorizeSecurityGroupIngress(event, context)
        elif event['detail']['eventName'] == 'AuthorizeSecurityGroupEgress':
            AuthorizeSecurityGroupEgress(event, context)
        elif event['detail']['eventName'] == 'CreateAccessKey':
            checkAccessKeyCreation(event, context)
        elif event['detail']['eventName'] == 'ConsoleLogin':
            ConsoleLoginDetectMain(event, context)
        elif event['detail']['eventName'] in ["StopLogging", "DeleteTrail"]:
            cloudTrail(event, context)
        elif event['detail']['eventName'] in ["CreateFunction20150331", "UpdateFunctionConfiguration20150331v2", "UpdateFunctionCode20150331v2"]:
            functionEvent(event, context)
        elif event['detail']['eventSource'] == 'ec2.amazonaws.com' and event['detail']['eventName'] == 'ModifySnapshotAttribute':
            EC2PublicSnapshot(event, context)
        elif event['detail']['eventSource'] == 'ec2.amazonaws.com' and event['detail']['eventName'] == 'ModifyImageAttribute':
            EC2PublicAMI(event, context)
        elif event['detail']['eventSource'] == 'ec2.amazonaws.com' and event['detail']['eventName'] == 'RunInstances':
            EC2PublicInstance(event, context)
        elif event['detail']['eventSource'] == 'rds.amazonaws.com' and event['detail']['eventName'] == 'ModifyDBClusterSnapshotAttribute':
            RDSPublicSnapshot(event, context)
        elif event['detail']['eventSource'] == 'rds.amazonaws.com' and event['detail']['eventName'] == 'ModifyDBSnapshotAttribute':
            RDSPublicSnapshot(event, context)
        elif event['detail']['eventSource'] == 'rds.amazonaws.com' and event['detail']['eventName'] == 'CreateDBInstance':
            RDSPublicInstance(event, context)
        elif event['detail']['eventSource'] == 'ec2.amazonaws.com' and event['detail']['eventName'] == 'CreateSecurityGroup':
            EC2PublicSecurityGroup(event, context)
        elif event['detail']['eventName'] == 'DeleteAccessKey':
            CheckAccessKeyDeletion(event, context)
        elif event['detail']['eventName'] == 'CreateLoadBalancer':
            CheckALBScheme(event, context)
        elif event['detail']['eventName'] == 'CreateVpc':
            CheckVpcCreate(event, context)
        elif event['detail']['eventName'] == 'DeleteVpc':
            CheckVpcDelete(event, context)
        elif event['detail']['eventName'] == 'CreateSubnet':
            CheckSubnet(event, context)
        elif event['detail']['eventName'] == 'DeleteSubnet':
            CheckSubnetDelete(event, context)
        elif event['detail']['eventName'] == 'CreateNatGateway':
            CheckNatGatewayCreate(event, context)
        elif event['detail']['eventName'] == 'DeleteNatGateway':
            CheckNatGatewayDelete(event, context)
        elif event['detail']['eventName'] == 'CreateRouteTable':
            CheckRouteTableCreate(event, context)
        elif event['detail']['eventName'] == 'DeleteRouteTable':
            CheckRouteTableDelete(event, context)
        elif event['detail']['eventName'] == 'DeleteHostedZone':
            CheckHostedZone(event, context)
        elif event['detail']['eventName'] == 'ChangeResourceRecordSets' and event['detail']['requestParameters']['changeBatch']['changes'][0]['action'] == 'DELETE':
            CheckRecords(event, context)
        elif event['detail']['eventName'] == 'DeleteSecret':
            CheckSecret(event, context)
        elif event['detail']['eventName'] == 'DeleteBackupVault':
            CheckBackupVault(event, context)
        elif event['detail']['eventName'] == 'DeleteBackupPlan':
            CheckBackupPlan(event, context)
        elif event['detail']['eventName'] == 'CreateVpcPeeringConnection':
            CheckVpcPeeringCreate(event, context)
        elif event['detail']['eventName'] == 'DeleteVpcPeeringConnection':
            CheckVpcPeeringDelete(event, context)
        elif event['detail']['eventName'] == 'CreateRepository':
            CheckEcr(event, context)
        elif event['detail']['eventName'] == 'CreateNetworkAcl':
            CheckNaclCreate(event, context)
        elif event['detail']['eventName'] == 'DeleteNetworkAcl':
            CheckNaclDelete(event, context)
        elif event['detail']['eventName'] == 'AllocateAddress':
            CheckElasticIpCreation(event, context)
        elif event['detail']['eventName'] == 'DeleteVpcEndpoints':
            CheckEndpoint(event, context)
        elif event['detail']['eventName'] == 'ReleaseAddress':
            CheckElasticIpDeletion(event, context)
        elif event['detail']['eventName'] == 'CreateUser':
            CreateIamUser(event, context)
        elif event['detail']['eventName'] == 'DeleteUser':
            DeleteIamUser(event, context)
        else:
            send_error(event, context, "Unhandled case")
    except Exception as e:
        print(e)
        send_error(event, context, str(traceback.format_exc()))

def AuthorizeSecurityGroupIngress(event, context):
    import AuthorizeSecurityGroupIngress_File as inner_fun
    response = inner_fun.AuthorizeSecurityGroupIngress_Inner(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def AuthorizeSecurityGroupEgress(event, context):
    import AuthorizeSecurityGroupEgress as inner_fun
    response = inner_fun.AuthorizeSecurityGroupEgress(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def checkAccessKeyCreation(event, context):
    import accessKeyCheck as inner_fun
    response = inner_fun.accessKeyCheckHandler(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def ConsoleLoginDetectMain(event, context):
    import ConsoleLoginDetect as inner_fun
    response = inner_fun.ConsoleLoginDetectHandler(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def PutBucketPublicAccessBlock(event, context):
    import BucketPublicAccess as inner_fun
    response = inner_fun.PutBucketPublicAccessBlock(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def cloudTrail(event, context):
    import cloudTrail_File as inner_fun
    response = inner_fun.cloudtrail(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def functionEvent(event, context):
    import function as inner_fun
    response = inner_fun.evaluate(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def send_error(event, context, message):
    import error_handler as error
    arn = context.invoked_function_arn
    event_region = arn.split(':')[3]
    account_id = arn.split(':')[4]
    error.send_message(event, event_region, account_id, message)

def EC2PublicSnapshot(event, context):
    import EC2PublicSnapshot as inner_fun
    response = inner_fun.get_ec2_modify_snapshot_public(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def EC2PublicAMI(event, context):
    import EC2PublicAMI as inner_fun
    response = inner_fun.get_ec2_modify_image_public(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def EC2PublicInstance(event, context):
    import EC2PublicInstance as inner_fun
    response = inner_fun.get_ec2_instance_public(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def RDSPublicSnapshot(event, context):
    import RDSPublicSnapshot as inner_fun
    response = inner_fun.get_rds_modify_snapshot_public(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def RDSPublicInstance(event, context):
    import RDSPublicInstance as inner_fun
    response = inner_fun.get_rds_instance_public(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def EC2PublicSecurityGroup(event, context):
    import EC2PublicSecurityGroup as inner_fun
    response = inner_fun.get_ec2_public_security_group(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckAccessKeyDeletion(event, context):
    import accessKeyCheckDeletion as inner_fun
    response = inner_fun.accessKeyCheckHandler(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckALBScheme(event, context):
    import ALBPublic as inner_fun
    response = inner_fun.get_alb_scheme(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckVpcCreate(event, context):
    import GetVpcDetail as inner_fun
    response = inner_fun.get_vpc_detail_create(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckVpcDelete(event, context):
    import GetVpcDetail as inner_fun
    response = inner_fun.get_vpc_detail_delete(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckSubnet(event, context):
    import GetSubnetDetail as inner_fun
    response = inner_fun.get_subnet_detail_create(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckNatGatewayCreate(event, context):
    import GetNatGatewayDetail as inner_fun
    response = inner_fun.get_natgateway_detail_create(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckNatGatewayDelete(event, context):
    import GetNatGatewayDetail as inner_fun
    response = inner_fun.get_natgateway_detail_delete(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)


def CheckRouteTableCreate(event, context):
    import GetRouteTableDetail as inner_fun
    response = inner_fun.get_route_table_detail_create(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckRouteTableDelete(event, context):
    import GetRouteTableDetail as inner_fun
    response = inner_fun.get_route_table_detail_delete(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckHostedZone(event, context):
    import GetHostedZoneDetail as inner_fun
    response = inner_fun.get_hostedZone_detail(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckRecords(event, context):
    import GetRecordsDetail as inner_fun
    response = inner_fun.get_Records_detail(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckSubnetDelete(event, context):
    import GetSubnetDetail as inner_fun
    response = inner_fun.get_subnet_detail_delete(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckSecret(event, context):
    import GetSecretDetail as inner_fun
    response = inner_fun.get_secret_detail(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckBackupPlan(event, context):
    import GetBackupPlanDetail as inner_fun
    response = inner_fun.get_backupplan_detail(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckBackupVault(event, context):
    import GetBackupVaultDetail as inner_fun
    response = inner_fun.get_backupvault_detail(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckVpcPeeringCreate(event, context):
    import GetVpcPeeringDetail as inner_fun
    response = inner_fun.get_vpcpeering_detail_create(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckVpcPeeringDelete(event, context):
    import GetVpcPeeringDetail as inner_fun
    response = inner_fun.get_vpcpeering_detail_delete(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckEcr(event, context):
    import GetEcrDetail as inner_fun
    response = inner_fun.get_ecr_detail(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckNaclCreate(event, context):
    import GetNaclDetail as inner_fun
    response = inner_fun.get_nacl_detail_create(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckNaclDelete(event, context):
    import GetNaclDetail as inner_fun
    response = inner_fun.get_nacl_detail_delete(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckElasticIpCreation(event, context):
    import GetAddressDetail as inner_fun
    response = inner_fun.get_address_create(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def CheckEndpoint(event, context):
    import GetEndpointDetail as inner_fun
    
    response = inner_fun.get_endpointdetail(event, context)
    print("reponse:", response)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)


def CheckElasticIpDeletion(event, context):
    import GetAddressDetail as inner_fun
    response = inner_fun.get_address_delete(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)


def CreateIamUser(event, context):
    import IamUserDetail as inner_fun
    response = inner_fun.get_user_details(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)

def DeleteIamUser(event, context):
    import IamUserDetail as inner_fun
    response = inner_fun.get_user_details(event, context)
    if response:
        notif = notification.evaluate(event, response)
        ses.send_mail(notif)


        