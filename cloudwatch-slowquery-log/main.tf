resource "aws_lambda_function" "lambda_function_service" {
  filename         = "${path.module}/function/lambda_function.zip"
  source_code_hash = data.archive_file.archive_function_obj.output_base64sha256
  function_name    = local.name
  role             = aws_iam_role.aws_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = var.runtime
  timeout          = var.timeout
  memory_size      = var.memory_size
  description      = var.description
  layers           = [aws_lambda_layer_version.lambda_layer.arn]
  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = var.sg_create ? [aws_security_group.lambda_sg[0].id] : var.security_group_ids
  }
  environment {
    variables = var.env_variables
  }
  tags = merge(local.tags, {
    "Name" = local.name
  })
  depends_on = [data.archive_file.archive_function_obj]
}

resource "aws_cloudwatch_log_group" "global_cloudwatch_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_function_service.function_name}"
  retention_in_days = var.retention_in_days
  tags = merge(local.tags, {
    "Name" = local.name
  })
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename                 = "${path.module}/layer/python_requirement.zip"
  layer_name               = local.name
  compatible_architectures = ["x86_64"]
  compatible_runtimes      = ["python3.10"]
}

resource "aws_lambda_permission" "lambda_permission_log" {
  for_each = {
    for lg in var.log_group_names :
    lg => {
      statement_id = "${regex("aws/rds/cluster/(.*?)(?:/slowquery)?$", lg)[0]}-slowquery-log"
      source_arn   = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:*:*"
    }
  }
  statement_id  = each.value.statement_id
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function_service.arn
  principal     = "logs.${data.aws_region.current.name}.amazonaws.com"
  source_arn    = each.value.source_arn
}

resource "aws_cloudwatch_log_subscription_filter" "lambda_function_logfilter" {
  for_each = {
    for lgn in var.log_group_names :
    lgn => {
      name           = "${regex("aws/rds/cluster/(.*?)(?:/slowquery)?$", lgn)[0]}-slowquery-log"
      log_group_name = "${lgn}"
    }
  }
  depends_on       = [aws_lambda_permission.lambda_permission_log]
  name             = each.value.name
  log_group_name   = each.value.log_group_name
  filter_pattern   = ""
  destination_arn  = aws_lambda_function.lambda_function_service.arn
  distribution     = "ByLogStream"
}
