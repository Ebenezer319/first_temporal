project_name = "<project name here>"
environment = "prod"  
maintainer = "<maintainer email here>"
region_name = "<region here>"
aws_account_id = "<accountId here>"

# Lambda Runtime
runtime = "python3.11"

temporal_example_lambda = {
    function_name = "temporal-example-s3-notification"
    description = "Example Function."
    handler = "lambda_function.example_function"
    timeout = 60
    memory_size = 128
}
