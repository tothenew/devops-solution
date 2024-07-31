

Follow these steps to set up this in your account.
[LINK](https://www.tothenew.com/blog/unlocking-efficiency-automated-aws-security-for-modern-businesses)

## Event Alerts
Here is the detailed use of event we are using.


| Event                              | Purpose
| ---------------------------------- |---------------------------------------------------------------------- |
| RunInstances                       | Get alert when any instance launches in a public subnet.              |
| ModifySnapshotAttribute            | Get alert when any EBS snapshot attributes are modified.              |
| ModifyImageAttribute               | Get alert when any AMI attributes are modified.                       |
| ModifyDBClusterSnapshotAttribute   | Get alert whenever changes apply to the public accessibility of RDS cluster snapshots. |
| ModifyDBSnapshotAttribute          | Get alert whenever changes apply to the public accessibility of RDS DB snapshots.      |
| CreateDBInstance                   | Get alert when a DB instance launches in a public subnet.             |
| CreateSecurityGroup                | Get alert whenever a security group rule allows traffic from 0.0.0.0/0.|
| AuthorizeSecurityGroupIngress      | Get alert whenever a security group rule allows ingress traffic from 0.0.0.0/0.         |
| AuthorizeSecurityGroupEgress       | Get alert whenever a security group rule allows egress traffic from 0.0.0.0/0.          |
| CreateAccessKey                    | Get alert whenever a new access key is created.                      |
| DeleteAccessKey                    | Get alert whenever an access key is deleted.                         |
| StopLogging                        | Get alert whenever logging in CloudTrail is stopped.                 |
| DeleteTrail                        | Get alert whenever a CloudTrail trail is deleted.                    |
| ConsoleLogin                       | Get alert whenever there is a console login.                         |
| PutBucketPublicAccessBlock         | Get alert when a public bucket is created.                           |
| PutBucketAcl                       | Get alert whenever a bucket ACL is modified.                         |
| CreateLoadBalancer                 | Get alert whenever a load balancer in a public subnet is created.     |
| CreateVpc                          | Get alert whenever a VPC is created.                                 |
| DeleteVpc                          | Get alert whenever a VPC is deleted.                                 |
| CreateSubnet                       | Get alert whenever a subnet is created.                              |
| DeleteSubnet                       | Get alert whenever a subnet is deleted.                              |
| CreateNatGateway                   | Get alert whenever a NAT gateway is created.                         |
| DeleteNatGateway                   | Get alert whenever a NAT gateway is deleted.                         |
| CreateRouteTable                   | Get alert whenever a route table is created.                         |
| DeleteRouteTable                   | Get alert whenever a route table is deleted.                         |
| DeleteHostedZone                   | Get alert whenever a hosted zone is deleted.                         |
| ChangeResourceRecordSets           | Get alert whenever records in a hosted zone are modified.            |
| DeleteSecret                       | Get alert whenever a secret is deleted.                              |
| DeleteBackupPlan                   | Get alert whenever a backup plan is deleted.                         |
| DeleteBackupVault                  | Get alert whenever a backup vault is deleted.                        |
| CreateVpcPeeringConnection         | Get alert whenever a VPC peering connection is created.              |
| DeleteVpcPeeringConnection         | Get alert whenever a VPC peering connection is deleted.              |
| CreateRepository                   | Get alert whenever a public repository is created.                   |
| CreateNetworkAcl                   | Get alert whenever a network ACL is created.                         |
| DeleteNetworkAcl                   | Get alert whenever a network ACL is deleted.                         |
| AllocateAddress                    | Get alert whenever an elastic IP is registered.                      |
| DeleteVpcEndpoints                 | Get alert whenever a VPC endpoint is deleted.                        |
| ReleaseAddress                     | Get alert whenever an elastic IP is deleted.                         |
