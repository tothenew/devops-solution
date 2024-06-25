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