# Metadata Tags
variable "tag_environment_name" {}
variable "tag_maintainer" {}
variable "tag_name" {}
variable "tag_run_always" {}
variable "tag_uniqueid" {}

# Variables
variable "description" {}
variable "name" {}
variable "execution_policy" {}
variable "handler" {}
variable "runtime" {}
variable "timeout" {}
variable "memory_size" {}
variable "queue_arn" {}

# Output
output "queue_lambda" {
  value = aws_lambda_function.lambda
}