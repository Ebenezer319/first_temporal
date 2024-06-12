data "template_file" "sqs_permission_policy" {
    template = file("${path.module}/sqs_policy.json")

    vars = {
      region_name    = var.region_name
      aws_account_id = var.aws_account_id
      queue_name     = aws_sqs_queue.queue.name
      source_arn     = var.source_arn
    }
}

resource "aws_sqs_queue_policy" "queue_policy" {
    queue_url = aws_sqs_queue.queue.id
    policy = data.template_file.sqs_permission_policy.rendered
}

resource "aws_sqs_queue" "queue" {
    name = var.queue_name
    visibility_timeout_seconds = var.timeout * 6
    sqs_managed_sse_enabled = true
    redrive_policy = "{\"deadLetterTargetArn\":\"${aws_sqs_queue.dlq.arn}\",\"maxReceiveCount\":50}"
    
    tags = {
        Environment = var.tag_environment_name
        Maintainer  = var.tag_maintainer
        Name        = var.tag_name
        Run_always  = var.tag_run_always
        UniqueID    = var.tag_uniqueid
    }

    depends_on = [ aws_sqs_queue.dlq ]
}

resource "aws_sqs_queue" "dlq" {
    name = "${var.queue_name}-dlq"
    visibility_timeout_seconds = var.timeout * 6
    sqs_managed_sse_enabled = true

    tags = {
        Environment = var.tag_environment_name
        Maintainer  = var.tag_maintainer
        Name        = var.tag_name
        Run_always  = var.tag_run_always
        UniqueID    = var.tag_uniqueid
    }
}