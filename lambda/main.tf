## LAMBDA
data "archive_file" "lambda" {
  type        = "zip"
  source_file = "lambda_function.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "get_data_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "lambda_function_payload.zip"
  function_name = "lambda_by_terraform"
  role          = var.lambda_role_arn
  handler       = "lambda_function.lambda_handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.9"
  timeout = "30"

  layers = ["arn:aws:lambda:eu-central-1:336392948345:layer:AWSSDKPandas-Python39:6", "arn:aws:lambda:eu-central-1:597570747370:layer:newsapi-boto3-libraries:1"]

  environment {
    variables = {
      api_key = var.api_key
    }
  }
}