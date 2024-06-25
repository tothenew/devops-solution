locals {
  name = var.name == "" ? "${terraform.workspace}-cw-slowquery-logs" : "${var.name}-cw-slowquery-logs"
  tags = length(var.common_tags) == 0 ? var.default_tags : merge(var.default_tags, var.common_tags)
}