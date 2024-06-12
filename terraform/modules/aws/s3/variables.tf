#MetaData
variable "tag_environment_name" {}
variable "tag_maintainer" {}
variable "tag_name" {}
variable "tag_run_always" {}
variable "tag_uniqueid" {}

#Variables
variable "bucket_name" {}
variable "bucket_acl" {
    default = "private"
}
variable "queue" {}
variable "notification_queue_arn" {}
variable "notification_filter_prefix" {}

#Outputs
output "bucket_name" {
    value = aws_s3_bucket.bucket.id
}
output "bucket_arn" {
    value = aws_s3_bucket.bucket.arn  
}
output "bucket" {
    value = aws_s3_bucket.bucket  
}

