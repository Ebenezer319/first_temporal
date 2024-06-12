variable "project_name" {
    type = string
    description = "Name of current project"
}
variable "maintainer" {
  type = string
}
variable "environment"{
}
variable "runtime"{}
variable "region_name"{}
variable "aws_account_id"{}
variable "run_always" {
  default = false
}

variable "temporal_example_lambda"{
    type = map(any)
}
variable "bucket_name"{}