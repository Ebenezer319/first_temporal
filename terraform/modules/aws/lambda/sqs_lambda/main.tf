data "template_file" "trust_policy" {
    template = file("${path.module}/execution_role_trust.json")
}

resource "aws_iam_role" "lambda_execution_role" {
    name = "${var.name}-role"
    assume_role_policy = data.template_file.trust_policy.rendered  
}

resource "aws_iam_role_policy" "lambda_execution_role" {
    name = "${var.name}-policy"
    policy = var.execution_policy
    role = aws_iam_role.lambda_execution_role.id

    depends_on = [aws_iam_role.lambda_execution_role]
}

resource "aws_lambda_function" "lambda" {
    filename = "${path.module}/invalid.zip"
    function_name = var.name
    role = aws_iam_role.lambda_execution_role.arn
    description = var.description
    publish = true
    handler = var.handler
    timeout = var.timeout
    memory_size = var.memory_size
    runtime = var.runtime

    tags = {
      Environment = var.tag_environment_name
      Maintainer = var.tag_maintainer
      Name = var.tag_name
      Run_Always = var.tag_run_always
      UniqueID = var.tag_uniqueid    
    }

    environment {
      variables = {
          tda_environment = var.tag_environment_name
      }
    }

    lifecycle {
      ignore_changes = [filename, layers]
    }

    depends_on = [
        aws_iam_role.lambda_execution_role,
        aws_iam_role_policy.lambda_execution_role
    ]  
}

resource "aws_lambda_alias" "prod_alias" {
    name = "prod"
    description = "Production Alias"
    function_name = aws_lambda_function.lambda.arn
    function_version = "$LATEST"

    lifecycle {
      ignore_changes = [function_version]
    }

    depends_on = [aws_lambda_function.lambda]
  
}

resource "aws_lambda_event_source_mapping" "sqs_queue_trigger" {
  batch_size = "1"
  event_source_arn = var.queue_arn
  function_name = aws_lambda_function.lambda.arn

  depends_on = [aws_lambda_function.lambda]  
}