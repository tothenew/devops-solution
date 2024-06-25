resource "aws_iam_role" "aws_role" {
  name               = "${local.name}-role"
  description        = "lambda role access"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  tags = merge(local.tags, { "Name" = "${local.name}-role" })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "${local.name}-policy"
  path        = "/"
  description = "${local.name}-policy"
  policy      = data.template_file.es_lambda_role.rendered
  tags = merge(local.tags, {
    "Name" = "${local.name}"
  })
}

resource "aws_iam_role_policy_attachment" "lambda_role_policy_attachment1" {
  role       = aws_iam_role.aws_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}
