#MetaData
variable "tag_environment_name" {}
variable "tag_maintainer" {}
variable "tag_name" {}
variable "tag_run_always" {}
variable "tag_uniqueid" {}

#Variables
variable "aws_account_id" {}
variable "region_name" {}
variable "queue_name" {}
variable "source_arn" {}
variable "timeout" {}

#Output
output "queue_arn" {
    value = aws_sqs_queue.queue.arn
}
output "queue" {
    value = aws_sqs_queue.queue
}

