variable "tag_environment_name" {}
variable "tag_maintainer" {}
variable "tag_project_name" {}
variable "tag_run_always" {}
variable "tag_uniqueid" {}

output "tag_environment" {
  value = var.tag_environment_name
}

output "tag_project_name" {
    value = var.tag_project_name
}

output "tag_uniqueid" {
  value = random_id.uniqueid.b64_std
}

output "tag_run_always" {
  value = var.tag_run_always
}