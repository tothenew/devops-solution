resource "aws_security_group" "lambda_sg" {
  count       = var.sg_create ? 1 : 0
  name        = "${local.name}-lamda-sg"
  description = "lamda security group"
  vpc_id      = var.vpc_id
  tags        = merge(local.tags, tomap({ "Name" : "${local.name}-lamda-sg" }))

  dynamic "egress" {
    for_each = data.aws_subnet.sn
    content {
      from_port   = 9200
      to_port     = 9200
      protocol    = "tcp"
      cidr_blocks = [egress.value.cidr_block]
      description = "Allow traffic to S3 Endpoints"
    }
  }
}
