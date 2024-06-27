import logging
import os
import json
from botocore.exceptions import ClientError

white_list_port=[80,443,53]
def AuthorizeSecurityGroupIngress_Inner(event, context):
    """Main Lambda hander - evaluates control and makes messaging decisions."""
    setup_logging()
    log.info('Got an event!')
    log.info(json.dumps(event, indent=2))
    cidr_violations = evaluate_control(event)
    if cidr_violations:
        log.info("Sending Violation for:"
                 + str(json.dumps(cidr_violations, indent=2)))
        message=invoke_alert(event, context, cidr_violations)
        return (message)

def evaluate_control(event):
    """Check to see of CIDR IP Range contains 0.0.0.0/0 or ::/0."""
    log.info('In Evaluate Control')
    cidr_violations = []
    try:
        security_group_rules = (event['detail']['requestParameters']
                                ['ipPermissions']['items'])
    except KeyError:
        log.info('Security group rules not found in the event.')
        return cidr_violations
    if "groupId" in event['detail']["requestParameters"]:
        security_group_identifier = (event['detail']["requestParameters"]
                                     ["groupId"])
    elif "groupName" in event['detail']["requestParameters"]:
        security_group_identifier = (event['detail']["requestParameters"]
                                     ["groupName"])
    else:
        log.warning('No VPC Security Group ID or Classic Security Group Name \
Found.')
    for rule in security_group_rules:
        cidr_violations = ipv4_checks(security_group_identifier, rule,
                                      cidr_violations)
        cidr_violations = ipv6_checks(security_group_identifier, rule,
                                      cidr_violations)

    return cidr_violations


def ipv4_checks(security_group_identifier, rule, cidr_violations):
    """IPv4 Checks."""
    try:
        for ipRange in rule['ipRanges']['items']:
            if ipRange['cidrIp'] == '0.0.0.0/0':
                log.info('Violation - Contains IP/CIDR of 0.0.0.0/0')
                cidr_ip = ipRange["cidrIp"]
                create_violation_list(security_group_identifier, rule,
                                      cidr_ip, cidr_violations)

    except KeyError:
        log.warning('There is not any Items under ipRanges')

    return cidr_violations


def ipv6_checks(security_group_identifier, rule, cidr_violations):
    """IPv4 Checks."""
    try:
        for ipv6Range in rule['ipv6Ranges']['items']:
            if ipv6Range['cidrIpv6'] == '::/0':
                log.info('Violation - Contains CIDR IPv6 equal to ::/0')
                cidr_ip = ipv6Range["cidrIpv6"]
                create_violation_list(security_group_identifier, rule,
                                      cidr_ip, cidr_violations)

    except KeyError:
        log.warning('There is not any Items under ipv6Ranges')

    return cidr_violations


def invoke_alert(event, context, cidr_violations):
    """Invoke Alerts and Actions."""
    log.info(event)
    event_details = []
    for resource in cidr_violations:
        if not resource["toPort"] in white_list_port:
            detail={
                "ResourceID": resource["groupIdentifier"],
                "ToPort": resource["toPort"],
                "FromPort": resource["fromPort"],
                "ipRange": resource["cidrIp"]
                }
            event_details.append(detail)
    return event_details


def create_violation_list(security_group_identifier,
                          rule, cidr_ip, cidr_violations):
    """Create Violation List."""
    if rule["ipProtocol"] == '-1':
        rule["toPort"]=0
        rule["fromPort"]=65535
    cidr_violations.append({
        "groupIdentifier": security_group_identifier,
        "ipProtocol": rule["ipProtocol"],
        "toPort": rule["toPort"],
        "fromPort": rule["fromPort"],
        "cidrIp": cidr_ip
    })
    return cidr_violations

def create_non_compliance_message(event, cidr_violations):
    """Create Non Compliance Message."""
    log.info("In Create Non Compliance Message")
    subject = "Violation - Security group rule contain a CIDR with /0!"
    message = "Violation - The following Security Group rules were in \
violation of the security group ingress policy and have an ingress rule with \
a CIDR of /0. \n\n"
    for resource in cidr_violations:
        message += 'Security Group Id: ' + resource["groupIdentifier"] + ' \n'
        message += 'IP Protocol: ' + resource["ipProtocol"] + ' \n'
        message += 'To Port: ' + str(resource["toPort"]) + ' \n'
        message += 'From Port: ' + str(resource["fromPort"]) + ' \n'
        message += 'CIDR IP: ' + str(resource["cidrIp"]) + ' \n'
        message += 'Account: ' + event['detail']['userIdentity']["accountId"]
        message += '\nRegion: ' + event['detail']["awsRegion"] + '\n\n\n'

    return subject, message
def setup_logging():
    """
    Logging Function.

    Creates a global log object and sets its level.
    """
    global log
    log = logging.getLogger()
    log_levels = {'INFO': 20, 'WARNING': 30, 'ERROR': 40}

    if 'logging_level' in os.environ:
        log_level = os.environ['logging_level'].upper()
        if log_level in log_levels:
            log.setLevel(log_levels[log_level])
        else:
            log.setLevel(log_levels['ERROR'])
            log.error("The logging_level environment variable is not set to INFO, WARNING, or \
                    ERROR.  The log level is set to ERROR")
    else:
        log.setLevel(log_levels['ERROR'])
        log.warning('The logging_level environment variable is not set. The log level is set to \
                  ERROR')
    log.info('Logging setup complete - set to log level '
             + str(log.getEffectiveLevel()))
