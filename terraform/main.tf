terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.4.6"
}

provider "aws" {
  profile = "<enter profile here>"
  region  = "<enter region here>"
}

module "metadata" {
  source = "./modules/metadata"

  tag_environment_name = var.environment
  tag_maintainer = var.maintainer
  tag_project_name = var.project_name
  tag_run_always = var.run_always
  tag_uniqueid = module.metadata.tag_uniqueid
}

data "template_file" "execution_policy" {
  template = file("${path.module}/execution_policy.json")

  vars = {
    region_name = var.region_name
    aws_account_id = var.aws_account_id
  }
}

module "ts_dependency_layer" {
  source = "./modules/aws/lambda/layers"

  lambda_dependency_layer_name = "${var.project_name}-layer"
  runtime = var.runtime  
}


#S3 Notification Objects
module "example_bucket" {
  source = "./modules/aws/s3"
  
  bucket_name                = var.bucket_name
  queue                      = modue.bucket_notification_queue
  notification_queue_arn     = modue.bucket_notification_queue.queue_arn
  notification_filter_prefix = "bucket-name/"

  tag_environment_name = module.metadata.tag_environment
  tag_maintainer = module.metadata.tag_maintainer
  tag_name = module.metadata.tag_project_name
  tag_run_always = module.metadata.tag_run_always
  tag_uniqueid = module.metadata.tag_uniqueid
}

module "bucket_notification_queue" {
  source = "./modules/aws/sqs"

  region_name = var.region_name
  aws_account_id = var.aws_account_id
  queue_name = "some-queue-name"
  timeout = var.temporal_example_lambda["timeout"]
  source_arn = module.example_bucket.bucket.arn

  tag_environment_name = module.metadata.tag_environment
  tag_maintainer = module.metadata.tag_maintainer
  tag_name = module.metadata.tag_project_name
  tag_run_always = module.metadata.tag_run_always
  tag_uniqueid = module.metadata.tag_uniqueid
}

module "temporal_example_lambda" {
  source = "./modules/aws/lambda/sqs_lambda"

  name = var.temporal_example_lambda["function_name"]
  description = var.temporal_example_lambda["description"]
  handler = var.temporal_example_lambda["handler"]
  memory_size = var.temporal_example_lambda["memory_size"]
  timeout = var.temporal_example_lambda["timeout"]
  runtime = var.runtime
  queue_arn = module.bucket_notification_queue.queue_arn
  execution_policy = data.template_file.execution_policy.rendered

  tag_environment_name = module.metadata.tag_environment
  tag_maintainer = var.maintainer
  tag_name = module.metadata.tag_project_name
  tag_run_always = module.metadata.tag_run_always
  tag_uniqueid = module.metadata.tag_uniqueid
}