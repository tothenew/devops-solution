# AWS Lambda CloudWatch Slow Query Log

This Terraform module facilitates the deployment of an AWS Lambda function designed for capturing and logging slow queries in CloudWatch.

## Usages

```hcl
module "cloudwatch-slowquery-log" {
  source = "git::git@github.com:tothenew/devops-solution.git//lambda/cloudwatch-slowquery-log?ref=master"
  name   = "dev-demo"
  log_group_names = ["/aws/rds/cluster/xxxxxxxxx/slowquery","/aws/rds/cluster/xxxxxxxxxxx/slowquery"]
  subnet_ids = ["subnet-xxxxxxxx","subnet-xxxxxxxxxx"]
  security_group_ids = ["sg-xxxxxxxxx"]
  env_variables = {
    ELASTICSEARCH_HOST = "10.25.xx.xx"
    ELASTICSEARCH_PORT = 9200
  }
  common_tags   = {
    "Environment" = "dev",
    "Project" = "Demo"
  }
}
```

## Requirements

| Name                              | Version   |
| --------------------------------- | --------- |
| [terraform](#requirement\_terraform) | >= 1.6.6  |
| [aws](#requirement\_aws)             | >= 5.32.1 |

## Providers

| Name               | Version   |
| ------------------ | --------- |
| [aws](#provider\_aws) | >= 5.32.1 |

## Resources

| Name                                                 | Type     |
| ---------------------------------------------------- | -------- |
| aws_lambda_function.lambda_function_service          | resource |
| aws_cloudwatch_log_group.global_cloudwatch_log_group | resource |
| aws_lambda_function_event_invoke_config              | resource |
| aws_cloudwatch_event_rule.cloudwatch_event_rule      | resource |
| aws_cloudwatch_event_target.cloudwatch_event_target  | resource |
| aws_lambda_permission                                | resource |

## Data Resources

| Name                | Type          |
| ------------------- | ------------- |
| aws_caller_identity | data resource |
| aws_region          | data resource |
| template_file       | data resource |
| archive_file        | data resource |
| aws_subnet          | data resource |

## Input

| Name                         | Description                                   | Type             | Default                                           | Required |
| ---------------------------- | --------------------------------------------- | ---------------- | ------------------------------------------------- | :------: |
| name                         | Prefix for the project name                   | `string`       | `"Dev"`                                         |    no    |
| default_tags                 | A map to add common tags to all resources     | `map(string)`  | `{ "Scope": "VPC", "CreatedBy": "Terraform" }`  |    no    |
| common_tags                  | A map to add common tags to all resources     | `map(string)`  | `{}`                                            |    no    |
| runtime                      | Runtime for Lambda function                   | `string`       | `"python3.10"`                                  |    no    |
| timeout                      | Timeout for Lambda function                   | `number`       | `120`                                           |    no    |
| memory_size                  | Memory size for Lambda function               | `number`       | `128`                                           |    no    |
| description                  | Description for the Lambda function           | `string`       | `"Cloudwatch Slow Query Logs to Elasticsearch"` |    no    |
| retention_in_days            | Retention period in days                      | `number`       | `7`                                             |    no    |
| maximum_event_age_in_seconds | Maximum event age in seconds                  | `number`       | `3600`                                          |    no    |
| maximum_retry_attempts       | Maximum retry attempts                        | `number`       | `0`                                             |    no    |
| schedule_expression          | Schedule expression for CloudWatch Events     | `string`       | `"cron(0 10 ? * 2 *)"`                          |    no    |
| rule_enabled                 | Flag to enable or disable the rule            | `bool`         | `true`                                          |    no    |
| env_variables                | Environment variables for the Lambda function | `map(string)`  | n/a                                               |   yes   |
| security_group_ids           | Lambda security group provided by the user    | `any`          | `null`                                          |    no    |
| sg_create                    | Flag to create SG for Lambda                  | `bool`         | `false`                                         |    no    |
| vpc_id                       | Required if creating SG                       | `any`          | `null`                                          |    no    |
| subnet_ids                   | Subnet IDs                                    | `any`          | n/a                                               |   yes   |
| log_group_names              | RDS log group names                           | `list(string)` | n/a                                               |   yes   |

## Outputs

| Name       | Description                                            |
| ---------- | ------------------------------------------------------ |
| lambda_arn | The Amazon Resource Name (ARN) of the Lambda function. |
