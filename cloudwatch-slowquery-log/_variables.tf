variable "name" {
  description = "Prefix for the project name"
  type        = string
  default     = "Dev"
}

variable "default_tags" {
  type        = map(string)
  description = "A map to add common tags to all the resources"
  default = {
    "Scope" : "VPC"
    "CreatedBy" : "Terraform"
  }
}

variable "common_tags" {
  type        = map(string)
  description = "A map to add common tags to all the resources"
  default     = {}
}

variable "runtime" {
  description = "Runtime for Lambda function"
  type        = string
  default     = "python3.10"
}

variable "timeout" {
  description = "Timeout for Lambda function"
  type        = number
  default     = 120
}

variable "memory_size" {
  description = "Memory size for Lambda function"
  type        = number
  default     = 128
}

variable "description" {
  description = "Description for the Lambda function"
  type        = string
  default     = "Cloudwatch Slow Query Logs to Elasticsearch"
}

variable "retention_in_days" {
  description = "Retention period in days"
  type        = number
  default     = 7
}

variable "maximum_event_age_in_seconds" {
  description = "Maximum event age in seconds"
  type        = number
  default     = 3600
}

variable "maximum_retry_attempts" {
  description = "Maximum retry attempts"
  type        = number
  default     = 0
}

variable "schedule_expression" {
  description = "Schedule expression for CloudWatch Events"
  type        = string
  default     = "cron(0 10 ? * 2 *)"
}

variable "rule_enabled" {
  description = "Flag to enable or disable the rule"
  type        = bool
  default     = true
}

variable "env_variables" {
  type = map(string)
}

variable "security_group_ids" {
  description = "Lamda security group provided by User"
  default     = null
}

variable "sg_create" {
  description = "SG for lamda"
  type        = bool
  default     = false
}
variable "vpc_id" {
  description = "Required If creating SG"
  default     = null
}
variable "subnet_ids" {}

variable "log_group_names" {
  description = "Rds log_group name"
  type = list(string)
}