data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "template_file" "es_lambda_role" {
  template = file("${path.module}/lambda-policy.tpl")

  vars = {
    account_id = data.aws_caller_identity.current.account_id
    region     = data.aws_region.current.name
    role_name  = aws_iam_role.aws_role.name
  }
}

data "aws_subnet" "sn" {
  for_each = var.sg_create ? toset(var.subnet_ids) : []
  id       = each.value
}

data "archive_file" "archive_function_obj" {
  type        = "zip"
  source_dir  = "${path.module}/function"
  output_path = "${path.module}/function/lambda_function.zip"
}